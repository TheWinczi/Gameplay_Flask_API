from frontend.src import app
from flask import Flask
import os

# app = Flask(None)

from werkzeug.datastructures import FileStorage


def __is_player_image_extension_valid(ext: str):
    """ Check is player image extension valid.

    Parameters
    ----------
    ext : str
        Extension of image. Should be in format '.<extension>'.

    Returns
    -------
    valid : bool
        Is provided image extension valid.
    """
    if not isinstance(ext, str):
        return False

    allowed_exts = app.config.get("PLAYER_IMAGE_FILE_ALLOWED_EXTENSIONS", (".jpg", ".png", ".bmp", ".jpeg"))
    if ext.lower() not in allowed_exts:
        return False

    return True


def __is_player_image_size_valid(size: int):
    """ Check is player image size valid.

    Parameters
    ----------
    size : int
        Size of the image.

    Returns
    -------
    valid : bool
        Is provided image size valid.
    """
    if not isinstance(size, int):
        return False

    max_sized = app.config.get("MAX_CONTENT_SIZE", 200*200)
    if size > max_sized:
        return False

    return True


def is_player_image_valid(image: FileStorage):
    """ Check is player image valid.

    Parameters
    ----------
    image : FileStorage
        Image to check.

    Returns
    -------
    valid : bool
        Is provided image valid.
    """
    if not isinstance(image, FileStorage):
        return False

    _, image_ext = os.path.splitext(image.filename)
    if not __is_player_image_extension_valid(image_ext):
        return False

    if not __is_player_image_size_valid(image.content_length):
        return False

    return True

