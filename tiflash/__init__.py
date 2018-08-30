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
from tiflash.core import    (   get_connections,
                                get_devices,
                                get_cpus,
                                list_options,
                                get_option,
                                get_bool_option,
                                get_float_option,
                                reset,
                                erase,
                                verify,
                                flash,
                                memory_read,
                                memory_write,
                                evaluate,
                                attach,

                                TIFlashError
                            )

from tiflash.version import version_string as __version__

__author__ = "Cameron Webb (webbjcam@gmail.com)"


# Remove any imported modules we don't want exported
del version
del core
