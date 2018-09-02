"""
helper module for xds110 specifc functions


Author: Cameron Webb
Date: March 2018
Contact: webbc92@gmail.com

"""
import os
import re
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


def xds110reset(ccs_path, serno=None):
    """Calls the xds110reset.exe in the xds110 directory

    Args:
        ccs_path (str): full path to ccs installation directory
        serno (str, optional): serial number to call xds110reset.exe on.
            If not found the first xds110 connection found will be used

    Returns:
        bool: True if successful/False if unsuccessful

    Raises:
        XDS110Error: raises if xds110reset.exe fails
    """
    xds_dir = get_xds110_dir(ccs_path)
    xds_exe = [ os.path.abspath(xds_dir + '/' + 'xds110reset') ]

    if not os.path.exists(xds_exe[0]):
        raise XDS110Error("Could not find xds110reset executable (%s)"
            % xds_exe)

    if serno:
        xds_exe.extend(['-s', serno])

    proc = subprocess.Popen(xds_exe, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    ret = proc.returncode

    if ret != 0:
        raise XDS110Error(out)

    return ret == 0


def xds110list(ccs_path):
    """Returns list of xds110 devices connected to the PC

    Uses xdsdfu -e command and parses output for sernos

    Args:
        ccs_path (str): full path to ccs installation directory

    Returns:
        list: list of sernos of the XDS110 devices connected

    Raises:
        XDS110Error: raises if xdsdfu.exe does not exist or fails
    """
    serno_pattern = "Serial Num\:\s+([A-Z0-9]{8})"
    regex = re.compile(serno_pattern)

    xds_dir = get_xds110_dir(ccs_path)
    xds_exe = [ os.path.abspath(xds_dir + '/' + 'xdsdfu') ]

    if not os.path.exists(xds_exe[0]):
        raise XDS110Error("Could not find xdsdfu executable (%s)"
            % xds_exe)

    xds_exe.extend(['-e'])

    proc = subprocess.Popen(xds_exe, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    ret = proc.returncode

    if ret != 0:
        raise XDS110Error(out)

    matches = re.findall(regex, out)

    return matches


def xds110upgrade(ccs_path):
    pass
