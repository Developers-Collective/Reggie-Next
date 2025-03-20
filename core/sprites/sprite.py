import enum

import spritelib as slib

__SPRITE_REGISTRY__ = {}
__NAME_TO_SPRITE__ = {}

__DEFAULT_ALPHA__ = 1.0
__DEFAULT_SCALE__ = 1.5
__DEFAULT_OFFSET__ = (0, 0)


class Offset(enum.Enum):
    """
    Predefined offset modes, which may be selected
    to adjust the render position of the sprite.
    """

    # Tries to adjust the position of the
    # so that it is drawn centered around
    # the cursor
    IMAGE_CENTER = 0

    # Tries to align the vertical position
    # to the lower edge of the grid
    SNAP_TO_Y = 1

    @classmethod
    def calculate_offset(cls, image, __t) -> tuple:
        match __t:
            case Offset.IMAGE_CENTER:
                return 10 - (image.width() / 4), 10 - (image.height() / 4)
            case Offset.SNAP_TO_Y:
                return 0, 10 - (image.height() / 2)


def get_registered_sprites() -> dict[int, (slib.SpriteImage | slib.SpriteImage_Static)]:
    from copy import deepcopy
    return deepcopy(__SPRITE_REGISTRY__)


def _create_static(cls: type, sprite_id: int, base_sprite: str = None, *, preloaded: bool = False,
                   initial_img: str = None, load_files: dict[str, str] = None, show_sprite_box: bool = False,
                   offset: (tuple | Offset) = None, alpha: float = None, scale: float = None, __dir: dict = None,
                   z: int = None, tile: int = None, bounding_rect: tuple = None) -> type:
    if sprite_id in __SPRITE_REGISTRY__:
        raise ValueError(f'A sprite with the id "{sprite_id}" is already registered')

    if cls.__name__ in __NAME_TO_SPRITE__:
        raise ValueError(f'A sprite with the name "{cls.__name__}" is already registered')

    is_extended = base_sprite is not None
    parent_class = __NAME_TO_SPRITE__[base_sprite] if is_extended else slib.SpriteImage_Static
    new_cls = type(cls.__name__, (cls, parent_class,), {})

    if is_extended:
        preloaded = parent_class.__pre_loaded__
        initial_img = parent_class.__initial_img__ if not initial_img else initial_img
        load_files = parent_class.__load_files__ if not load_files else (parent_class.__load_files__ | load_files)
        z = parent_class.__z__ if not z else z
        alpha = parent_class.__alpha__ if not alpha else alpha
        offset = parent_class.__offset__ if not offset else offset
        scale = parent_class.__scale__ if not scale else scale

    if not alpha:
        alpha = __DEFAULT_ALPHA__

    if not scale:
        scale = __DEFAULT_SCALE__

    new_cls.__pre_loaded__ = preloaded
    new_cls.__initial_img__ = initial_img
    new_cls.__load_files__ = load_files

    new_cls.__z__ = z
    new_cls.__offset__ = offset
    new_cls.__scale__ = scale
    new_cls.__alpha__ = alpha

    def __init__(self, parent) -> None:
        slib.SpriteImage_Static.__init__(self, parent=parent, scale=scale)
        self.spritebox.shown = show_sprite_box

        # Setting the tile gives priority
        if tile:
            self.image = slib.GetTile(tile)
        else:
            if initial_img is not None:
                if isinstance(initial_img, list):
                    self.image = [slib.ImageCache[img] for img in initial_img]
                else:
                    self.image = slib.ImageCache[initial_img]
            else:
                try:
                    self.image = slib.ImageCache[parent_class.__name__] if is_extended else slib.ImageCache[cls.__name__]
                except KeyError:
                    if not preloaded and len(load_files) > 1:
                        self.image = None
                    else:
                        print(f'Unable to load sprite image "{cls.__name__}"')

        if isinstance(offset, Offset):
            self.offset = Offset.calculate_offset(self.image, offset)
        else:
            self.offset = offset if offset else __DEFAULT_OFFSET__

        self.alpha = alpha
        if z:
            parent.setZValue(z)

        if bounding_rect is not None:
            print(bounding_rect)
            self.aux.append(slib.AuxiliaryImage(parent, bounding_rect[0], bounding_rect[1]))

    new_cls.__init__ = __init__
    new_cls.loadImages = staticmethod(lambda: ...)
    if load_files:
        def loadImages():
            for name, file in load_files.items():
                slib.loadIfNotInImageCache(name, file)

        new_cls.loadImages = __dir.get('loadImages', staticmethod(loadImages))

    new_cls.dataChanged = __dir.get('dataChanged', slib.SpriteImage_Static.dataChanged)
    new_cls.paint = __dir.get('paint', slib.SpriteImage_Static.paint)

    __SPRITE_REGISTRY__[sprite_id] = new_cls
    __NAME_TO_SPRITE__[new_cls.__name__] = new_cls
    return new_cls


def static_sprite(sprite_id: int, base_sprite: str = None, *, preloaded: bool = False,
                  initial_img: str | list[str] = None, load_files: dict[str, str] = None, show_sprite_box: bool = False,
                  offset: (tuple | Offset) = None, alpha: float = None, scale: float = None,
                  z: int = None, tile: int = None, bounding_rect: tuple = None):
    def decorator(cls):
        return _create_static(cls, sprite_id, base_sprite=base_sprite, preloaded=preloaded,
                              initial_img=initial_img, load_files=load_files, offset=offset, alpha=alpha, scale=scale,
                              z=z, tile=tile, show_sprite_box=show_sprite_box, bounding_rect=bounding_rect,
                              __dir={method: getattr(cls, method) for method in dir(cls) if not method.startswith("__")})

    return decorator


def create_static_sprite(class_name: str, sprite_id: int, base_sprite: str = None, *, preloaded: bool = False,
                         initial_img: str = None, load_files: dict[str, str] = None, show_sprite_box: bool = False,
                         offset: (tuple | Offset) = None, alpha: float = None, scale: float = None,
                         __dir: dict = None, z: int = None, bounding_rect: tuple = None,
                         tile: int = None) -> type:
    cls = type(class_name, (), {})
    cls_dict = {method: getattr(cls, method) for method in dir(cls) if not method.startswith("__")}
    return _create_static(cls, sprite_id, base_sprite, preloaded=preloaded, initial_img=initial_img,
                          load_files=load_files, offset=offset, alpha=alpha, scale=scale, z=z, tile=tile,
                          __dir=cls_dict, show_sprite_box=show_sprite_box, bounding_rect=bounding_rect)

