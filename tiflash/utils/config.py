"""
helper module for retrieving configuration settings


Author: Cameron Webb
Date: Sept 2019
Contact: webbjcam@gmail.com

"""
import os

DEFAULT_TIFLASH_FOLDER = "~/.tiflash"
DEFAULT_CUSTOM_FOLDER = "custom"

def init_config_dirs():
    """Creates .tiflash base folder as well as any configuration subfolders
    inside of it.

    Note:
        Typically only used by setup.py when pip installing package
    """
    base = get_base_dir()
    custom = get_custom_dir()

    if not os.path.exists(base):
        os.mkdir(base)

    if not os.path.exists(custom):
        os.mkdir(custom)



def get_base_dir():
    """Returns the path to the .tiflash folder

    Returns:
        str: full path to the .tiflash folder
    """

    return os.path.expanduser(DEFAULT_TIFLASH_FOLDER)

def get_custom_dir():
    """Returns the path to the custom folder inside .tiflash folder

    Returns:
        str: full path to the .tiflash/custom folder
    """

    return os.path.join(get_base_dir(), DEFAULT_CUSTOM_FOLDER)
