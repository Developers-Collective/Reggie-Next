import os.path

import globals_

__ROOT_PATH__ = globals_.ROOT_PATH


def load_resource_as_text(name: str, *, relative_path: str = None) -> list[str]:
    relative_path = '' if not relative_path else relative_path
    return open(os.path.join(__ROOT_PATH__, 'reggiedata', relative_path, name), 'r').readlines()


def load_resource_as_str(name: str, *, relative_path: str = None, delimiter: str = '') -> str:
    return delimiter.join(load_resource_as_text(name, relative_path=relative_path))
