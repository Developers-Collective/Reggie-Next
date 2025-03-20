from itertools import repeat
from pathlib import Path

import globals_
import spritelib as SLib
from mj2d.course.area import Area
from revolution.arc.u8 import Arc


class AbstractLevel:
    """
    Class for an abstract level from any game. Defines the API.
    """

    def __init__(self):
        """
        Initializes the level with default settings
        """
        self.filepath = None
        self.name = 'untitled'

        self.areas = []

    def load(self, data, areaNum):
        """
        Loads a level from bytes data. You MUST reimplement this in subclasses!
        """
        pass

    def save(self):
        """
        Returns the level as a bytes object. You MUST reimplement this in subclasses!
        """
        return b''

    def deleteArea(self, number):
        """
        Removes the area specified. Number is a 1-based value, not 0-based;
        so you would pass a 1 if you wanted to delete the first area.
        """
        del self.areas[number - 1]

        # change all later areas to use the correct num
        for i, area in enumerate(self.areas, 1):
            area.set_num(i)

        return True

    def changeArea(self, number):
        """
        Changes the current area to the specified area in the loaded level
        archive. Note that number is 1-based, not 0-based.
        """
        return False


class Level_NSMBW(AbstractLevel):
    """
    Class for a level from New Super Mario Bros. Wii
    """

    def __init__(self):
        """
        Initializes the level with default settings
        """
        super().__init__()
        self.new(False)

    def new(self, load=True):
        """
        Creates a completely new level
        """
        # Create area objects
        self.areas = []

        new_area = Area(1)

        if load:
            new_area.load_defaults()

        globals_.Area = new_area
        SLib.Area = new_area

        self.areas.append(new_area)

    def load(self, data, areaToLoad):
        """
        Loads a NSMBW level from bytes data.
        """
        super().load(data, areaToLoad)

        arc = Arc.from_file(data, load_files_raw=True)

        if "course" not in arc:
            return False

        areas = [[None for _ in repeat(None, 4)] for _ in repeat(None, 4)]
        for file_name, file in arc['course'].items():
            name = Path(file_name).stem

            area_id = int(name.replace('course', '')[0])

            # Something invalid was read, skip it
            if not (1 <= area_id <= 4):
                continue

            # We look, if we have either the layer data
            # so a file like courseX_bgdatLX.bin or not
            if name[-2] == 'L':
                areas[area_id - 1][int(name[-1]) + 1] = file
            else:
                areas[area_id - 1][0] = file

        # Create area objects
        self.areas = []
        for i, data in enumerate(areas, 1):
            course, L0, L1, L2 = data

            if course is None:
                continue

            new_area = Area(i)
            new_area.set_data(course, L0, L1, L2)
            self.areas.append(new_area)

        self.areas[areaToLoad - 1].load()
        globals_.Area = self.areas[areaToLoad - 1]
        SLib.Area = self.areas[areaToLoad - 1]

        return True

    def save(self):
        """
        Save the level back to a file
        """

        # Make a new archive
        newArchive = Arc()

        # Create a folder within the archive
        newArchive['course'] = None

        # Go through the areas, save them and add them back to the archive
        for i, area in enumerate(self.areas):
            assert area.areanum == i + 1, (area.areanum, i + 1)

            course, L0, L1, L2 = area.save()

            # Layers 0 and 2 are optional, but the game assumes that the course
            # file and layer 1 will always exist (see dBg_c::CheckExistLayer())
            newArchive.append_file(f'course{area.areanum}.bin', course, path='course/')

            if L1 is None:
                newArchive.mkdir(f'course/course{area.areanum}_bgdatL1.bin')
            else:
                newArchive.append_file(f'course{area.areanum}_bgdatL1.bin', L1, path='course/')

            if L0 is not None:
                newArchive.append_file(f'course{area.areanum}_bgdatL0.bin', L0, path='course/')

            if L2 is not None:
                newArchive.append_file(f'course{area.areanum}_bgdatL2.bin', L2, path='course/')

        # return the U8 archive data
        return newArchive.to_bytes()

    def appendArea(self, course_new, L0_new, L1_new, L2_new):
        """
        Creates a new area and adds it to the current level.
        """
        # Add new area
        new_area = Area(len(self.areas) + 1)
        new_area.set_data(course_new, L0_new, L1_new, L2_new)
        self.areas.append(new_area)

    def changeArea(self, number):
        """
        Changes the current area to the specified area in the loaded level
        archive. Note that number is 1-based, not 0-based.
        """
        current_num = globals_.Area.areanum

        # self.areas[current_num - 1] should be unloaded.
        self.areas[current_num - 1].unload()

        # Set the globals properly
        globals_.Area = self.areas[number - 1]
        SLib.Area = self.areas[number - 1]

        # self.areas[number - 1] should be loaded.
        self.areas[number - 1].load()

        return True

