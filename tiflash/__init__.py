"""
TIFlash
Licensed under the MIT license (see `LICENSE` file)

A (unofficial) python module for flashing TI devices.
"""
from tiflash.core import (
    TIFlashSession,
    TIFlashError,
    get_connections,
    get_devicetypes,
    get_cpus,
    get_option,
    set_option,
    list_options,
    reset,
    erase,
    verify,
    flash,
    memory_read,
    memory_write,
    register_read,
    register_write,
    evaluate,
    attach,
    xds110_reset,
    xds110_list,
    xds110_upgrade,
    detect_devices,
    get_info,
)

from tiflash.version import version_string as __version__

__author__ = "Cameron Webb (webbjcam@gmail.com)"


# Remove any imported modules we don't want exported
del version
del core
