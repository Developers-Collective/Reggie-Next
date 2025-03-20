import dataclasses
import io
import itertools
import os
import shutil
from collections import deque
from pathlib import Path
from struct import unpack
from typing import BinaryIO, Self, Any

U8_FILE_MAGIC = "Uª8-"


def _align(x, boundary):
    rem = x % boundary

    if rem != 0:
        x += boundary - rem

    return x


@dataclasses.dataclass
class _FST_ENTRY_:
    is_dir: bool
    name_off: int
    parent_or_file_off: int
    next_entry_or_len: int

    def to_binary(self) -> bytes:
        is_dir_byte = (1 if self.is_dir else 0).to_bytes(1, "big")

        if not (0 <= self.name_off <= 0xFFFFFF):
            raise ValueError("name_off must fit into 24 bits (0..16777215).")
        name_off_bytes = self.name_off.to_bytes(3, "big")

        parent_off_bytes = self.parent_or_file_off.to_bytes(4, "big")
        next_len_bytes = self.next_entry_or_len.to_bytes(4, "big")

        return is_dir_byte + name_off_bytes + parent_off_bytes + next_len_bytes

    @classmethod
    def load_from_bin(cls, __src: BinaryIO) -> Self:
        is_dir_name_off, parent_or_file_off, next_entry_or_len = unpack('>III', __src.read(12))
        return cls(bool(is_dir_name_off & 0xff000000),
                   is_dir_name_off & 0x00ffffff,
                   parent_or_file_off,
                   next_entry_or_len)


@dataclasses.dataclass
class ArcFile:
    name: str
    data: bytes | bytearray

    @property
    def file_size(self) -> int:
        return len(self.data) if self.data else 0

    def to_file(self, path: str) -> None:
        with open(path, 'wb') as __out:
            __out.write(self.data)

    def __len__(self) -> int:
        return self.file_size

    def __str__(self) -> str:
        return f'ArcFile<{self.name}, file_size={self.file_size} bytes>'

    def __repr__(self) -> str:
        return self.__str__()


class Arc:
    def __init__(self, *, data: (BinaryIO | None) = None, load_files_raw: bool = False) -> None:
        # number of modifications on this ARC file
        self._mod_count = 0

        # general fields
        self._flat_file_struct = {}
        self._only_files = {}

        if data is not None:
            self._created_manually = False
            self._load_from_bin(data, load_files_raw)
        else:
            self._created_manually = True
            self._arc_name = 'ARC_FILE'
            self.files = {}

    def _update(self) -> None:
        if self._mod_count > 0:
            self._mod_count = 0
            self._only_files = self._flatten_file_map()
            self._flat_file_struct = self._flatten_file_map(include_dirs=True)

    def _load_from_bin(self, data: BinaryIO, load_files_raw: bool) -> None:
        if isinstance(data, BinaryIO):
            self._arc_name = data.name
        else:
            self._arc_name = 'ARC_FILE'

        base_offset = data.tell()
        file_magic = unpack('>4s', data.read(4))[0].decode('latin1')

        if file_magic != U8_FILE_MAGIC:
            raise AssertionError(f"Read wrong file magic for U8 file: {file_magic}")

        fst_start, fst_size, file_start = unpack('>iii', data.read(12))
        data.read(16)  # Skip reserved bytes

        string_tbl_start = 0

        def open_arc() -> list[_FST_ENTRY_]:
            _fst_start = base_offset + fst_start

            data.seek(_fst_start)
            head = _FST_ENTRY_.load_from_bin(data)

            entry_num = head.next_entry_or_len  # in this case the length
            nodes = [_FST_ENTRY_.load_from_bin(data) for _ in range(entry_num - 1)]
            nodes.insert(0, head)

            # Read the string table
            nonlocal string_tbl_start
            string_tbl_start = data.tell()

            return nodes

        def read_terminated_string(encoding='ascii') -> str:
            stream = iter(lambda: data.read(1), b'')
            taken = itertools.takewhile(lambda b: b != b'\x00', stream)
            return b''.join(taken).decode(encoding)

        entries = open_arc()
        __len = entries[0].next_entry_or_len - 1

        already_parsed = []
        self.files = {}

        def load_dir(__dir_idx: int, __path: str) -> dict[Any, Any]:
            already_parsed.append(__dir_idx)  # Remember this dir already being parsed
            dir_files = {}         # all files of this exact directory
            dir_stack = deque([])  # stack of directories, currently being processed

            __dir = entries[__dir_idx]  # The root dir where processing will start

            # We process all files and sub dirs until we reach the
            # end, which is defined by the len field of the directory
            #
            # We start processing by the next index, so we do not include
            # the starting dir itself in the file entry dict
            current_dir = dir_files  # We start processing at the top-level dir
            current_path = __path    # The relative file path of this directory

            for x in range(__dir_idx + 1, __dir.next_entry_or_len):
                already_parsed.append(x)  # Remember this entry being parsed already
                __entry = entries[x]

                # Fetch name of the current file/dir entry
                data.seek(string_tbl_start + __entry.name_off)
                __name = read_terminated_string()

                if __entry.is_dir:
                    # We have an empty dir
                    if __entry.next_entry_or_len == (x + 1):
                        current_dir[__name] = {}
                    # Otherwise we have a dir with data, so we make this dir
                    # the current target dir for all files
                    else:
                        sub_dir = {}
                        current_dir[__name] = sub_dir

                        current_dir = sub_dir
                        current_path = os.sep.join([current_path, __name])

                        dir_stack.append((__entry.next_entry_or_len, sub_dir, __path))
                else:
                    data.seek(__entry.parent_or_file_off)
                    if load_files_raw:
                        __file = data.read(__entry.next_entry_or_len)
                    else:
                        __file = ArcFile(__name, data.read(__entry.next_entry_or_len))

                    current_dir[__name] = __file

                # Check if we reached the end of this dir
                # if yes, pop the dir from the stack, so we do not
                # work on it anymore.
                while dir_stack and dir_stack[-1][0] == x + 1:
                    dir_stack.pop()

                # If we still have dirs left, we work on the next higher
                # dir in the hierarchy, otherwise, we work directly on
                # the starting dir.
                if dir_stack:
                    current_dir = dir_stack[-1][1]
                    current_path = dir_stack[-1][2]
                else:
                    current_dir = dir_files
                    current_path = __path

            return dir_files

        for i in range(1, entries[0].next_entry_or_len):
            if i in already_parsed:
                continue

            entry = entries[i]
            if entry.is_dir:
                data.seek(string_tbl_start + entry.name_off)
                name = read_terminated_string()

                self.files[name] = load_dir(i, os.sep + name)
            else:
                already_parsed.append(i)

                data.seek(string_tbl_start + entry.name_off)
                name = read_terminated_string()

                if load_files_raw:
                    self.files[name] = data.read(entry.next_entry_or_len)
                else:
                    self.files[name] = ArcFile(name, data.read(entry.next_entry_or_len))

        self._only_files = self._flatten_file_map()
        self._flat_file_struct = self._flatten_file_map(include_dirs=True)

    def _flatten_file_map(self, include_dirs: bool = False) -> dict[str, (ArcFile | None)]:
        results = {}

        stack = deque()
        stack.append((os.path.splitext(self._arc_name)[0], self.files))

        while stack:
            current_path, current_dict = stack.pop()

            if include_dirs:
                pass

            for key, value in current_dict.items():
                next_path = str(os.path.join(current_path, key))

                if isinstance(value, dict):
                    if include_dirs:
                        results[next_path] = None
                    stack.append((next_path, value))
                else:
                    results[next_path] = value

        return results

    def _rename_dict_key_in_place(self, d: dict, old_key: str, new_key: str) -> None:
        if old_key not in d:
            raise KeyError(f"No key '{old_key}' in dictionary to rename.")
        if new_key in d:
            raise KeyError(f"Key '{new_key}' already exists in dictionary.")

        keys = list(d.keys())
        idx = keys.index(old_key)

        val = d[old_key]
        del d[old_key]

        keys[idx] = new_key

        new_dict = {}
        for k in keys:
            if k == new_key:
                new_dict[new_key] = val
            else:
                new_dict[k] = d[k]

        d.clear()
        d.update(new_dict)

        self._mod_count += 1

    @classmethod
    def from_file(cls, src: (str | bytes | BinaryIO), *, load_files_raw: bool = False) -> Self:
        """
        Loads a U8 archive from either the given path or the given
        data buffer.  If load_files_raw is true, all files will not
        be loaded as 'ArcFile' objects but only their bytes.
        """
        if isinstance(src, bytes):
            return cls(data=io.BytesIO(src), load_files_raw=load_files_raw)

        return cls(data=open(src, 'rb'), load_files_raw=load_files_raw) if isinstance(src, str) \
            else cls(data=src, load_files_raw=load_files_raw)

    @property
    def arc_name(self) -> str:
        return Path(self._arc_name).stem

    def to_dir(self, __path: str = None) -> None:
        """
        Writes all data of this U8 archive at the specified file path as a folder
        structure. If the __path parameter is not given, the original path of the
        U8 file will be used instead. It will delete all old content.

        :param __path: (Optional) The path to write this archive to. The name of the file
                       will either be determined by the arc_name field of this object, or
                       if a file name is already present in the __path, that file name
                       will be used instead.
        """
        self._update()
        if self._created_manually:
            target_path = __path
        else:
            target_path = os.path.splitext(__path if __path is not None else self._arc_name)[0]

        if os.path.exists(target_path):
            shutil.rmtree(target_path)  # Remove directory and all contents

        os.makedirs(target_path)
        if not self._flat_file_struct:
            self._flat_file_struct = self._flatten_file_map(include_dirs=True)

        for __p, __data in self._flat_file_struct.items():
            if __data is None:
                os.makedirs(os.path.join(target_path, __p))
            else:
                __data.to_file(os.path.join(target_path, __p))

    def to_bytes(self) -> bytes:
        """
        Write this U8 archive to a file at the specified path.

        U8 Layout:
          - 0x20-byte header:
              * Magic "U\xAA8-"
              * 4 bytes: offset to FST (big-endian)
              * 4 bytes: size of FST
              * 4 bytes: offset to file data
              * 16 bytes: reserved
          - FST (File System Table): 12 bytes per entry, back-to-back
          - String table: immediately after the FST, *no* padding
          - File data: each file’s contents, aligned to 32 bytes
        """
        import struct

        # ---------------------------------------------
        # STEP 1. BUILD FST ENTRIES (PRE-ORDER TRAVERSAL)
        # ---------------------------------------------
        fst_entries: list[_FST_ENTRY_] = []
        names: list[str] = []
        file_map: dict[int, ArcFile] = {}

        def add_entry(name: str, is_dir: bool, parent_idx: int) -> int:
            """Append a placeholder FST entry, append name, and return its index."""
            idx = len(fst_entries)
            fst_entries.append(None)  # Will fill later
            names.append(name)
            return idx

        def traverse(name: str, node, parent_idx: int) -> None:
            """Recursively traverse 'node' (dict for folder or ArcFile for file)."""
            if isinstance(node, dict):
                # Directory
                my_idx = add_entry(name, True, parent_idx)
                for child_name, child_node in node.items():
                    traverse(child_name, child_node, my_idx)
                # After children, fill the directory entry:
                next_idx = len(fst_entries)
                fst_entries[my_idx] = _FST_ENTRY_(
                    is_dir=True,
                    name_off=0,
                    parent_or_file_off=parent_idx,
                    next_entry_or_len=next_idx
                )
            else:
                # File
                my_idx = add_entry(name, False, parent_idx)
                # We'll fill in offset/size below
                fst_entries[my_idx] = _FST_ENTRY_(
                    is_dir=False,
                    name_off=0,
                    parent_or_file_off=0,  # file offset
                    next_entry_or_len=0  # file size
                )
                file_map[my_idx] = node

        # Root directory has an empty name and "parent" = 0
        root_idx = add_entry("", True, 0)
        # Traverse all top-level entries
        for key, value in self.files.items():
            traverse(key, value, root_idx)
        # Fill in the root entry's next_entry_or_len to the total # of entries
        fst_entries[root_idx] = _FST_ENTRY_(
            is_dir=True,
            name_off=0,
            parent_or_file_off=0,  # root's parent is 0
            next_entry_or_len=len(fst_entries)
        )

        # ---------------------------------------------
        # STEP 2. BUILD STRING TABLE
        # ---------------------------------------------
        string_table = bytearray()
        name_offsets = []
        for nm in names:
            off = len(string_table)
            name_offsets.append(off)
            string_table.extend(nm.encode('ascii', errors='replace'))
            string_table.append(0)

        # Now that we have name offsets, assign them to each entry
        for idx, entry in enumerate(fst_entries):
            entry.name_off = name_offsets[idx]

        # ---------------------------------------------
        # STEP 3. CALCULATE OFFSETS
        # ---------------------------------------------
        # Official approach:
        #  * FST starts at offset 0x20 (immediately after header).
        #  * FST is NOT padded to 32 bytes.
        #  * The string table is directly after FST (alignment by 32 bytes).
        #  * The file data region is aligned to 32 bytes, immediately after the string table.
        fst_offset = 0x20
        fst_size = len(fst_entries) * 12
        str_table_offset = fst_offset + fst_size
        str_table_size = len(string_table)
        # File data offset is 32-byte aligned after string table
        file_data_offset = _align(str_table_offset + str_table_size, 0x20)

        # ---------------------------------------------
        # STEP 4. FILL FILE ENTRIES (offset & size)
        # ---------------------------------------------
        curr_file_off = file_data_offset
        for idx, entry in enumerate(fst_entries):
            if not entry.is_dir:
                arc_file = file_map[idx]
                entry.parent_or_file_off = curr_file_off

                if arc_file is None:
                    continue

                if isinstance(arc_file, ArcFile) and arc_file.data is not None:
                    entry.next_entry_or_len = len(arc_file.data)
                    curr_file_off += _align(len(arc_file.data), 0x20)
                else:
                    entry.next_entry_or_len = len(arc_file)
                    curr_file_off += _align(len(arc_file), 0x20)

        # ---------------------------------------------
        # STEP 5. WRITE EVERYTHING TO A BUFFER
        # ---------------------------------------------
        buffer = io.BytesIO()

        # Write 0x20-byte header
        # Format: magic, offsetToFST, fstSize, fileDataOffset, 16 reserved
        # Magic "U\xAA8-" => 0x55 0xAA 0x38 0x2D
        buffer.write(struct.pack(
            '>4sIII16s',
            U8_FILE_MAGIC.encode('latin-1'),  # magic
            fst_offset,  # offset to FST
            fst_size + str_table_size,  # size of FST
            file_data_offset,  # offset to file data
            b"\x00" * 16  # reserved
        ))

        # Write FST
        for entry in fst_entries:
            buffer.write(entry.to_binary())

        # Write string table (align to 32 bytes)
        buffer.write(string_table)
        pad = _align(len(buffer.getvalue()), 32) - len(buffer.getvalue())

        buffer.write(b'\x00' * pad)

        # Write file data, each file aligned to 32 bytes
        for idx, entry in enumerate(fst_entries):
            if not entry.is_dir:
                arc_file = file_map[idx]
                if isinstance(arc_file, ArcFile) and arc_file.data is not None:
                    if not isinstance(arc_file.data, bytes):
                        arc_file.data = b''

                    buffer.write(arc_file.data)
                    pad = _align(len(arc_file.data), 32) - len(arc_file.data)
                else:
                    buffer.write(arc_file)
                    pad = _align(len(arc_file), 32) - len(arc_file)

                if pad:
                    buffer.write(b'\x00' * pad)

        return buffer.getvalue()

    def write_to_file(self, out_path: str) -> None:
        with open(out_path, 'wb') as f:
            f.write(self.to_bytes())

    def get_all_files(self) -> dict[str, ArcFile]:
        """
        :return: All files of this archive in a list
        """
        self._update()
        return self._only_files

    def append_file(self, filename: str, file: (bytes | str), *, path: list[str] | str | None = None) -> None:
        """
        Append a file to this archive under the specified directory path (creating
        directories if needed). If 'path' is omitted or empty, the file is placed
        directly under the root.

        Args:
            filename (str): The key/name for this file in the final directory.
            file (ArcFile): The file object to insert (contains data, etc.).
            path (list[str] | str | None): A directory path, which may be:
                - None or an empty string/list, meaning "place in root".
                - A list of directory names, e.g. ["folderA", "subfolderB"].
                - A string like "folderA/subfolderB". (Split on '/' internally.)

        Raises:
            ValueError: If a path segment is already a file, or if 'file' is invalid.
            KeyError: If 'filename' already exists in the final directory.
        """
        if isinstance(file, str):
            file = open(file, 'rb').read()

        self._append_internal(filename, ArcFile(filename, file), path=path)

    def mkdir(self, path: list[str] | str) -> None:
        """
        Create a directory (and any necessary parent directories) at the specified path.
        If the directory already exists, nothing happens.

        :param path: The directory path, either as a list of names or a string separated by '/'.
        """
        self._get_or_create_directory(path)
        self._mod_count += 1

    def _get_or_create_directory(self, path: list[str] | str | None) -> dict:
        """
        Traverse the archive tree (self.files) following the given path.
        If any directory in the path does not exist, it is created.
        If path is None or empty, return the root directory (self.files).

        :param path: A list of directory names or a string with '/' as separator.
        :return: The dictionary corresponding to the final directory.
        :raises ValueError: If a path segment exists as a file.
        """
        if path is None:
            return self.files
        if isinstance(path, str):
            # Split on '/' and filter out any empty segments
            path = [seg for seg in path.split("/") if seg]
        current_dict = self.files
        for seg in path:
            if seg not in current_dict:
                # Create the directory if it doesn't exist.
                current_dict[seg] = {}
            else:
                # Ensure that this segment is a directory.
                if not isinstance(current_dict[seg], dict):
                    raise ValueError(f"Path segment '{seg}' exists as a file; cannot create directory here.")
            current_dict = current_dict[seg]
        return current_dict

    def _append_internal(self, filename: str, file: ArcFile, *, path: list[str] | str | None = None) -> None:
        target_dir = self._get_or_create_directory(path)
        if filename in target_dir:
            raise KeyError(
                f"A file or directory named '{filename}' already exists in the specified path."
            )
        target_dir[filename] = file
        self._mod_count += 1

    def rename(self, path: list[str] | str, new_name: str) -> None:
        """
        Rename a file or directory along the given path to 'new_name'.

        The 'path' parameter can be either:
          - A list of keys (str) from the root down to the item to rename, e.g.:
                ["FolderA", "SubFolder", "File1"]
          - A single string with '/' as a separator, e.g.:
                "FolderA/SubFolder/File1"

        :param path: The path to the item to rename.
        :param new_name: The new name for the final node in 'path'.
        :raises ValueError, KeyError: If the path is invalid or conflicts occur.
        """
        # Convert path to list of segments if necessary.
        if isinstance(path, str):
            path = [seg for seg in path.split("/") if seg]

        if not path:
            raise ValueError("Path cannot be empty (must specify at least one level).")

        # Separate into parent keys and the final key.
        *parents, old_key = path

        current_dict = self.files
        for key in parents:
            if key not in current_dict:
                raise KeyError(f"Path segment '{key}' not found.")
            sub = current_dict[key]
            if not isinstance(sub, dict):
                raise ValueError(f"Path segment '{key}' does not refer to a directory.")
            current_dict = sub

        if old_key not in current_dict:
            raise KeyError(f"No item '{old_key}' found in the specified path.")

        # Allow renaming for both directories and files.
        self._rename_dict_key_in_place(current_dict, old_key, new_name)

    def delete(self, path: list[str] | str) -> None:
        """
        Delete an element (file or directory) along the given 'path'.
        If the element is a directory, all of its contents are removed.

        The 'path' parameter can be either:
          - A list of keys (str) from the root down to the item to remove, e.g.:
                ["FolderA", "SubFolder", "File1"]
          - A single string with '/' as the separator, e.g.:
                "FolderA/SubFolder/File1"

        :param path: The path of the item to remove.
        :raises KeyError: If a path segment or final key doesn't exist.
        :raises ValueError: If a path segment is not a directory while descending.
        """
        # Convert a '/'-separated string into a list of segments.
        if isinstance(path, str):
            path = [seg for seg in path.split("/") if seg]

        if not path:
            raise ValueError("Path cannot be empty.")

        # Separate parent keys from the final key to delete.
        *parents, to_remove = path

        current_dict = self.files
        for key in parents:
            if key not in current_dict:
                raise KeyError(f"Path segment '{key}' does not exist.")
            sub = current_dict[key]
            if not isinstance(sub, dict):
                raise ValueError(f"Path segment '{key}' is not a directory.")
            current_dict = sub

        if to_remove not in current_dict:
            raise KeyError(f"No item '{to_remove}' found at final level.")

        # Delete the target node (file or directory)
        del current_dict[to_remove]
        self._mod_count += 1

    def move(self, src: list[str] | str, dest: list[str] | str) -> None:
        """
        Move an element (file or directory) from one location to another.

        Both src and dest can be provided as a list of strings (e.g. ["FolderA", "File1"])
        or as a '/'-separated string (e.g. "FolderA/File1"). The destination path is assumed to include
        the new name of the moved element. Any missing directories in the destination path will be created.

        For example:
          move("FolderA/File1", "FolderB/NewFile1")
        will move "File1" from FolderA to FolderB and rename it to "NewFile1".

        :param src: Source path to the element to move.
        :param dest: Destination path (including the new name).
        :raises KeyError: If the source path doesn't exist or destination already exists.
        :raises ValueError: If a path segment is not a directory.
        """
        # Convert source and destination to lists of segments if provided as strings.
        if isinstance(src, str):
            src = [seg for seg in src.split("/") if seg]
        if isinstance(dest, str):
            dest = [seg for seg in dest.split("/") if seg]

        if not src:
            raise ValueError("Source path cannot be empty.")
        if not dest:
            raise ValueError("Destination path cannot be empty.")

        # Split source path into parent segments and the source item name.
        *src_parents, src_name = src
        current_dict = self.files
        for seg in src_parents:
            if seg not in current_dict:
                raise KeyError(f"Source path segment '{seg}' not found.")
            if not isinstance(current_dict[seg], dict):
                raise ValueError(f"Source path segment '{seg}' is not a directory.")
            current_dict = current_dict[seg]

        if src_name not in current_dict:
            raise KeyError(f"Source item '{src_name}' not found.")

        # Remove the element from its source location.
        element = current_dict.pop(src_name)
        self._mod_count += 1

        # Split destination path into parent segments and destination name.
        *dest_parents, dest_name = dest
        dest_dict = self._get_or_create_directory(dest_parents)
        if dest_name in dest_dict:
            raise KeyError(f"Destination item '{dest_name}' already exists in the target directory.")

        # Insert the element into the destination dictionary under the new name.
        dest_dict[dest_name] = element
        self._mod_count += 1

    def __iter__(self) -> tuple[str, ArcFile]:
        for name, value in self._flat_file_struct.items():
            yield name, value

    def __len__(self) -> int:
        self._update()
        return len(self._flat_file_struct)

    def __contains__(self, item: str | list[str]) -> bool:
        """
        Check if a file or folder exists in the archive.

        The key can be provided as a single name, a '/'-separated string,
        or a list of strings representing the path.

        :param item: The path (or key) to check.
        :return: True if the item exists, False otherwise.
        """
        try:
            _ = self[item]
            return True
        except KeyError:
            return False

    def __getitem__(self, item) -> ...:
        """
        Retrieve a file or folder from the archive.

        The key can be provided either as:
          - A single name (for a top-level item),
          - A '/'-separated string (e.g. "Folder/SubFolder/File"),
          - Or a list of strings (e.g. ["Folder", "SubFolder", "File"]).

        :param item: The path to the file or folder.
        :return: The file (an ArcFile) or folder (a dict) corresponding to the given path.
        :raises KeyError: If any segment in the path is not found.
        """
        self._update()
        # Normalize item into a list of keys.
        if isinstance(item, str):
            # If there's a '/' present, split on it; otherwise, treat it as a single key.
            keys = [seg for seg in item.split("/") if seg] if "/" in item else [item]
        elif isinstance(item, list):
            keys = item
        else:
            raise KeyError("Invalid key type. Must be a string or list of strings.")

        current = self.files
        for key in keys:
            if key not in current:
                raise KeyError(f"Key '{key}' not found in archive.")
            current = current[key]
        return current

    def __setitem__(self, key, value) -> None:
        if value is self:
            raise RecursionError('U8 Arc Error: Cannot assign an archive to itself')

        if not isinstance(key, str):
            raise KeyError('U8 Arc Error: Can only have name values (strings) as keys')

        self._mod_count += 1

        if key in self.files and isinstance(self.files[key], dict):
            self.files[key][value.name] = value
        else:
            if value is None:
                self.files[key] = {}
            elif isinstance(value, Arc):
                self.files[key] = value.files
            elif isinstance(value, bytes) or isinstance(value, bytearray) or isinstance(value, ArcFile):
                self.files[key] = value
            else:
                self._mod_count -= 1
                raise ValueError(f'U8 Arc Error: Invalid value type for object in arc. Cannot add {type(value)} to arc files.')

    def __str__(self) -> str:
        def pretty_print_arc(structure: dict[str, (ArcFile | dict)], indent: int = 0) -> str:
            lines = []
            prefix = " " * (indent * 4)

            for key, value in structure.items():
                # We have a dir
                if isinstance(value, dict):
                    if value:
                        lines.append(f'{prefix}<dir: "{key}">')
                        lines.append(pretty_print_arc(value, indent + 1))
                    else:
                        lines.append(f'{prefix}<EMPTY dir: "{key}">')
                # We have a file
                else:
                    lines.append(f"{prefix}{key}")

            return "\n".join(lines)

        self._update()
        return f'<Arc="{self._arc_name}">\n{pretty_print_arc(self.files, 1)}'

    def __repr__(self) -> str:
        return self.__str__()
