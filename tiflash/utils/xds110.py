"""
helper module for xds110 specifc functions


Author: Cameron Webb
Date: March 2018
Contact: webbjcam@gmail.com

"""
import os
import platform
import re
import time
import subprocess

XDS110_DIRECTORY = "ccs_base/common/uscif/xds110"

class XDS110Error(Exception):
    """Generic XDS110 Error"""
    pass

def get_xds110_dir(ccs_path):
    """Returns full path to xds110 directory.

    Args:
        ccs_path (str): full path to ccs installation directory

    Returns:
        str: full path to xds110 directory

    Raises:
        XDS110Error: raises if xds110 directory cannot be found.
    """
    xds110_path = os.path.abspath(ccs_path + '/' + XDS110_DIRECTORY)
    if not os.path.isdir(xds110_path):
        raise XDS110Error("Could not find xds110 directory (%s)" % xds110_path)

    return xds110_path

def get_xds110_exe_path(ccs_path, exe):
    """Returns full path xds110 executable

    Args:
        ccs_path (str): full path to ccs installation directory
        exe (str): name of executable

    Returns:
        str: full path to xdsdfu executable

    Raises:
        XDS110Error: raises if xdsdfu executable cannot be found.
    """
    xds_dir = get_xds110_dir(ccs_path)
    xds_exe_path = os.path.abspath(xds_dir + '/' + exe)

    if platform.system() == "Windows":
        xds_exe_path += ".exe"

    if not os.path.exists(xds_exe_path):
        raise XDS110Error("Could not find xdsdfu executable (%s)"
            % xds_exe_path)

    return xds_exe_path


def xds110_reset(ccs_path, serno=None):
    """Calls the xds110reset.exe in the xds110 directory

    Args:
        ccs_path (str): full path to ccs installation directory
        serno (str, optional): serial number to call xds110reset.exe on.
            If no serno provided the first xds110 connection found will be used

    Returns:
        bool: True if successful/False if unsuccessful

    Raises:
        XDS110Error: raises if xds110reset.exe fails
    """
    xdsreset_path = get_xds110_exe_path(ccs_path, 'xds110reset')

    xds_exe = [ xdsreset_path ]


    if serno:
        xds_exe.extend(['-s', serno])

    proc = subprocess.Popen(xds_exe, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    ret = proc.returncode

    if ret != 0:
        raise XDS110Error(out)

    return ret == 0


def xds110_list(ccs_path):
    """Returns list of xds110 devices connected to the PC

    Uses xdsdfu -e command and parses output for sernos

    Args:
        ccs_path (str): full path to ccs installation directory

    Returns:
        list: list of tuples (sernos, version) of the XDS110 devices connected

    Raises:
        XDS110Error: raises if xdsdfu.exe does not exist or fails
    """
    serno_pattern = "Serial Num\:\s+([A-Z0-9]{8})"
    version_pattern = "Version\:\s+([0-9\.]+)"
    serno_regex = re.compile(serno_pattern)
    version_regex = re.compile(version_pattern)

    xdsdfu_path = get_xds110_exe_path(ccs_path, 'xdsdfu')
    xds_exe = [ xdsdfu_path]

    xds_exe.extend(['-e'])

    proc = subprocess.Popen(xds_exe, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    ret = proc.returncode

    if ret != 0:
        raise XDS110Error(out)

    serno_matches = re.findall(serno_regex, str(out))
    version_matches = re.findall(version_regex, str(out))

    matches = [ (serno_matches[i], version_matches[i])
                    for i in range(len(serno_matches)) ]

    return matches


def xds110_upgrade(ccs_path, serno=None):
    """Upgrades/Flashes XDS110 firmware on board.

    Firmware flashed is found in xds110 directory (firmware.bin). This function
    uses the 'xdsdfu' executable to put device in DFU mode. Then performs the
    flash + reset functions of xdsdfu to flash the firmware.bin image

    Args:
        ccs_path (str): full path to ccs installation directory
        serno (str, optional): serial number to flash firmware to.
            If no serno provided the first xds110 connection found will be used

    Returns:
        bool: True if successful/False if unsuccessful

    Raises:
        XDS110Error: raises if xds110 firmware update fails
    """
    xdsdfu_path = get_xds110_exe_path(ccs_path, 'xdsdfu')
    firmware_path = os.path.abspath(get_xds110_dir(ccs_path) + '/'+ "firmware.bin")

    if not os.path.exists(firmware_path):
        raise XDS110Error("Could not find firmware.bin file (%s)" %
            firmware_path)

    serno_list = [ s for (s,v) in xds110_list(ccs_path) ]
    xds_dfu_cmd = [ xdsdfu_path]
    xds_flash_cmd = [ xdsdfu_path]

    # Get Device Index using Serno
    if serno:
        try:
            index = serno_list.index(serno)
        except ValueError:
            raise XDS110Error("Device: %s not connected." % serno)

        xds_dfu_cmd += ['-i', str(index)]

        # After putting device in DFU mode, its index will be 0
        xds_flash_cmd += ['-i', '0']

    # Put device in DFU mode first
    xds_dfu_cmd += ['-m']

    proc = subprocess.Popen(xds_dfu_cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    ret = proc.returncode

    if ret != 100:
        raise XDS110Error(out)

    # Give time for device to enter DFU mode
    time.sleep(1)

    # Flash Firmware to Device
    xds_flash_cmd += ['-f', firmware_path, '-r']

    proc = subprocess.Popen(xds_flash_cmd, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    ret = proc.returncode

    if ret != 0:
        raise XDS110Error(out)

    return ret == 0
