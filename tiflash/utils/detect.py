"""Helper module used for detecting devices connected to PC"""

import os
import platform
system = platform.system()


if system == "Windows":
    import re
    if platform.python_version().startswith('2'):
        import _winreg as winreg
    else:
        import winreg
else:
    from serial.tools import list_ports


class DetectError(Exception):
    """Device Detection Error"""
    pass


def detect_devices():
    """Detect devices connected to machine.

    Returns:
        list: list of tuples containing device info.
            Tuple in the format of (vid, pid, serno)
    """
    devices = list()
    if system == "Windows":
        devices = _win_detect_devices()
    else:
        devices = _unix_detect_devices()

    # remove duplicates
    devices = list(set(devices))

    return devices


def detect_sernos():
    """Get list of connected device sernos

    Returns:
        list: list of device serial numbers
    """
    sernos = list()
    devices = detect_devices()

    for dev in devices:
        try:
            serno = get_serno_from_vidpid(dev[0], dev[1])
            sernos.append(serno)
        except Exception:
            pass

    return sernos


def get_serno_from_vidpid(vid, pid):
    """Get serno of device given vid and pid

    Args:
        vid (int): vid number of connection
        pid (int): pid number of connection

    Returns:
        str: device serial number
    """
    serno = None
    probe_list = None
    detected_devices = detect_devices()

    for dev in detected_devices:
        if vid == dev[0] and pid == dev[1]:
            serno = dev[2]
            break
    else:
        raise Exception("Was not able to find a connection with given vid (%s) and pid (%s)" % (vid, pid))


    return serno


def _win_detect_devices():
    """Windows only: Gets vid, pid and serno of each device connected

    Returns:
        list: list of tuples containing vid, pid and serno of each device
            connected.
    """
    device_list = list()
    ti_vidpid_pattern = "USB\\\\VID_([0-9a-fA-F]{4})&PID_([0-9a-fA-F]{4})\\\\([0-9A-Za-z]*)"
    ti_vidpid_re = re.compile(ti_vidpid_pattern)

    usbccgp_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
        r"SYSTEM\CurrentControlSet\Services\usbccgp\Enum")

    num_devices = winreg.QueryInfoKey(usbccgp_key)[1]
    for i in range(num_devices):
        dev_data = winreg.EnumValue(usbccgp_key, i)
        match = ti_vidpid_re.search(str(dev_data[1]))
        if match:
            dev = (int(match.group(1), 16), int(match.group(2), 16), match.group(3))
            device_list.append(dev)

    return device_list



def _unix_detect_devices():
    """Unix only: Gets vid, pid and serno of each device connected

    Returns:
        list: list of tuples containing vid, pid and serno of each device
            connected.
    """
    device_list = list()
    ports = list_ports.comports()

    for p in ports:
        dev = (p.vid, p.pid, p.serial_number)
        device_list.append(dev)

    return device_list
