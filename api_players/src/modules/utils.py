import os
import secrets

from werkzeug.datastructures import FileStorage


def save_image(image: FileStorage, dir_path: str):
    """ Save provided image on hard drive in /static/ directory.

    Parameters
    ----------
    image : FileStorage
        Image object to save.

    dir_path : str
        Path to directory for image.

    Returns
    -------
    image_fn : str
        Hashed image file name allows to get saved image from server.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(dir_path, image_fn)
    image.save(image_path)

    return image_fn


def remove_file(path: str):
    """ Remove file from provided path

    Parameters
    ----------
    path : str
        Path to image to remove.

    Returns
    -------
    removed : bool
        Was file removed from provided path.
    """
    if not isinstance(path, str):
        return False

    if os.path.exists(path):
        if os.path.isfile(path):
            try:
                os.remove(path)
                return True
            except FileNotFoundError | IsADirectoryError as e:
                return False
        else:
            return False
    else:
        return True


def get_image_bytes(image_path: str):
    """ Get bytes of player image with provided image filename

    Parameters
    ----------
    image_path : str
        Path to the image to get.

    Returns
    -------
    """
    if not isinstance(image_path, str):
        return []

    if os.path.exists(image_path):
        with open(image_path, 'rb') as image:
            return image.read()
    else:
        return []
