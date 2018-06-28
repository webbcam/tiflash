"""


 ________  ______  ________  __                      __
/        |/      |/        |/  |                    /  |
$$$$$$$$/ $$$$$$/ $$$$$$$$/ $$ |  ______    _______ $$ |____
   $$ |     $$ |  $$ |__    $$ | /      \  /       |$$      \
   $$ |     $$ |  $$    |   $$ | $$$$$$  |/$$$$$$$/ $$$$$$$  |
   $$ |     $$ |  $$$$$/    $$ | /    $$ |$$      \ $$ |  $$ |
   $$ |    _$$ |_ $$ |      $$ |/$$$$$$$ | $$$$$$  |$$ |  $$ |
   $$ |   / $$   |$$ |      $$ |$$    $$ |/     $$/ $$ |  $$ |
   $$/    $$$$$$/ $$/       $$/  $$$$$$$/ $$$$$$$/  $$/   $$/



TIFlash
Licensed under the MIT license (see `LICENSE` file)

A (unofficial) python module for flashing TI devices.

"""
from . import core
from .core import TIFlashError

from tiflash.version import version_string as __version__

__author__ = "Cameron Webb (webbjcam@gmail.com)"


# Remove any imported modules we don't want exported
del version
