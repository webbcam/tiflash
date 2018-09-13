"""
helper module for finding installed device types


Author: Cameron Webb
Date: March 2018
Contact: webbjcam@gmail.com

"""

import os
import re
import json

from tiflash.utils import xmlhelper

from tiflash.utils.connections import get_connections_directory
from tiflash.utils.cpus import get_cpus_directory

DEVICES_DIR = "/ccs_base/common/targetdb/devices"
BOARD_IDS_PATH = "/ccs_base/cloudagent/src/targetDetection/board_ids.json"

# Place this file in utils/ folder to use a custom board_ids file
CUSTOM_BOARD_IDS_FILE = "board_ids.json"


class DeviceError(Exception):
    """Generic Device Error"""
    pass


def get_devices_directory(ccs_path):
    """Returns full path to devices directory

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: full path to devices directory
    """
    devices_directory = os.path.normpath(ccs_path + "/" + DEVICES_DIR)

    if not os.path.exists(devices_directory):
        raise DeviceError("Could not find 'devices' directory.")

    return devices_directory


def get_device_xml_from_devicetype(devicetype, ccs_path):
    """Returns full path to device xml given a devicetype if exists, else returns None.

    Args:
        devicetype (str): devicetype to search xmls for
        ccs_path (str): path to ccs installation to use for searching xmls

    Returns:
        str or None: full path to device xml if exists, otherwise returns None

    Raises:
        DeviceError: raises exception if devices directory can not
            be found
    """
    device_xml = None

    # Get devices xmls
    device_xmls = get_device_xmls(ccs_path, full_path=True)

    for dxml in device_xmls:
        try:    # Some xmls are not valid device xml files
            device = get_devicetype(dxml)
        except Exception:
            continue

        if device == devicetype:
            device_xml = os.path.normpath(dxml)
            break

    else:
        raise DeviceError("Could not find device xml for %s. Please install "
                            "drivers for %s.""" % (devicetype, devicetype))

    return device_xml


def get_devicetype(device_xml):
    """Returns the devicetype from the device xml file

    Args:
        device_xml (str): full path to device xml file

    Returns:
        str: devicetype set in device xml file
    """
    devicetype = None
    root = __get_device_root(device_xml)

    if root.tag != "device":
        raise DeviceError("Error parsing devicetype from device xml: %s" %
                        device_xml)

    devicetype = xmlhelper.get_attrib_value(root.attrib, ["desc", "partnum", "id"])

    return devicetype


def get_cpu(device_xml):
    """Returns the cpu name from device xml file.

    Args:
        device_xml (str): full path to the device xml file to parse

    Returns:
        str: cpu name
    """
    cpu = None
    root = __get_device_root(device_xml)

    cpu_element = root.find(".//cpu")
    if cpu_element is None:
        raise DeviceError("Error parsing cpu from device xml: %s" % device_xml)

    cpu = xmlhelper.get_attrib_value(cpu_element.attrib, ["desc", "id"])

    return cpu


def get_default_connection_xml(device_xml, ccs_path):
    """Returns the default connection xml from the device xml file

    Args:
        device_xml (str): full path to device xml file

    Returns:
        str: default connection xml set in device xml file

    Raises:
        DeviceError: raised if device xml does not contain 'default connection'
    """
    connection_xml = None
    root = __get_device_root(device_xml)

    conn_element = root.find(".//property[@id='DefaultConnection']")

    if conn_element is None:
        raise DeviceError("Device XML: %s does not contain a Default "
                            "Connection type." % device_xml)

    xml_name = xmlhelper.get_attrib_value(conn_element.attrib, ["Value"])


    connection_xml = get_connections_directory(ccs_path) + '/' + xml_name
    connection_xml = os.path.normpath(connection_xml)

    return connection_xml


def get_device_xmls(ccs_path, full_path=False):
    """Gets a list of the device xmls files

    Args:
        ccs_path (str): path to ccs installation
        full_path (boolean, optional): returns full path of each device xml

    Returns:
        list: list of device xml files
    """
    device_dir = get_devices_directory(ccs_path)
    devices = [f for f in os.listdir(device_dir) if f.endswith('.xml')]

    if full_path:
        devices = [ os.path.abspath(device_dir + '/' + c) for c in devices ]

    return devices


def get_device_xml_path(xml_name, ccs_path):
    """Returns full path to device xml if exists, else returns None.

    Args:
        xml_name (str): name of device to search xmls for
        ccs_path (str): path to ccs installation to use for searching xmls

    Returns:
        str or None: full path to device xml if exists otherwise returns None

    Raises:
        deviceError: raises exception if device directory can not be found
    """
    device_xml = None

    if not xml_name.endswith('.xml'):
        xml_name += ".xml"

    device_xmls = get_device_xmls(ccs_path)

    if xml_name in device_xmls:
        device_xml = os.path.normpath(
                            get_devices_directory(ccs_path) + "/" + xml_name)

    return device_xml


def get_cpu_xml(device_xml, ccs_path):
    """Returns the full path to cpu xml specified in given device xml

    Args:
        device_xml (str): full path to device xml to parse

    Returns:
        str: full path to cpu xml
    """
    cpu_xml = None
    root = __get_device_root(device_xml)

    cpu_element = root.find(".//cpu")
    p_cpu_element = root.find(".//cpu/..")

    if cpu_element is None or p_cpu_element is None:
        raise DeviceError("Error parsing cpu from device xml: %s" % device_xml)

    instance_element = xmlhelper.get_sibling(cpu_element, p_cpu_element, -1)

    if instance_element is None:
        raise DeviceError("Error parsing instance-cpu from device xml: %s" % device_xml)

    xml_name = xmlhelper.get_attrib_value(instance_element.attrib, ["xml"])

    cpu_xml = get_cpus_directory(ccs_path) + '/' + xml_name
    cpu_xml = os.path.normpath(cpu_xml)

    return cpu_xml


def get_devicetypes(ccs_path):
    """ Returns list of installed device names.

    Searches "<ccs_path>/ccs_base/common/targetdb/devices" directory for
    installed device names.

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        list: device names

    Raises:
        DeviceError: raises exception if devices directory can not
            be found

    """
    #   Set Devices directory
    devices_directory = get_devices_directory(ccs_path)

    #   Get devices xmls
    device_xmls = get_device_xmls(ccs_path, full_path=True)

    device_list = list()
    for cxml in device_xmls:
        try:    # Some xmls are not valid device xml files
            device = get_devicetype(cxml)
        except Exception:
            continue
        device_list.append(device)

    return device_list


def find_device(device_name, ccs_path):
    """ Returns full device name(s) matching 'device_name'

    Uses regex to try to match given 'device_name' to all installed
    device types.

    Args:
        device_name (str): device name to try to match (i.e. xds110)
        ccs_path (str): full path to ccs installation to use

    Returns:
        list: list of full device names that matched the given
        device_name

    Raises:
        DeviceError: raises exception if CCS installation can not be found

    """
    devices = get_devicetypes(ccs_path)
    match_list = list()
    device_re = re.compile(device_name.lower())

    for d in devices:
        if device_re.search(d.lower()) is not None:
            match_list.append(d)

    return match_list


def get_device_xml_from_serno(serno, ccs_path):
    """ Returns full path to device xml determined by device serial no.

    Uses board_ids.json file to determine devicetype from serial no.

    Args:
        serno (str): device serial number
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: path to device xml determined from serial number

    Raises:
        DeviceError: raises exception if board_ids.json file can not be found
            in given CCS installation or if the devicetype can not be
            determined by given serial number

    """
    devices_directory = get_devices_directory(ccs_path)

    # Allow for using custom boards_id file by placing custom file in utils/
    custom_board_ids_path = os.path.normpath(os.path.dirname(__file__) + '/' +
                                             CUSTOM_BOARD_IDS_FILE)

    if os.path.isfile(custom_board_ids_path):
        board_ids_path = custom_board_ids_path
    else:
        board_ids_path = os.path.normpath(ccs_path + "/" + BOARD_IDS_PATH)

    if not os.path.isfile(board_ids_path):
        raise DeviceError("Could not find 'board_ids.json' file: %s"
                          % board_ids_path)

    with open(board_ids_path) as board_ids_f:
        board_ids = json.load(board_ids_f)

        sernos = board_ids.keys()
        for s in sernos:
            if serno.startswith(s):
                dxml = board_ids[s]['deviceXml'] + ".xml"
                break
        else:
            raise DeviceError(
                "Could not determine devicetype from %s." % serno)

        dxml_fullpath = os.path.abspath(devices_directory + "/" + dxml)
        if not os.path.isfile(dxml_fullpath):
            raise DeviceError("Could not find '%s' file." % dxml)

        return dxml_fullpath


def get_device_from_serno(serno, ccs_path):
    """ Returns full device name determined by device serial no.

    Uses board_ids.json file to determine devicetype from serial no.

    Args:
        serno (str): device serial number
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: devicetype determined from serial number

    Raises:
        DeviceError: raises exception if board_ids.json file can not be found
            in given CCS installation or if the devicetype can not be
            determined by given serial number

    """
    dxml_fullpath = get_device_xml_from_serno(serno, ccs_path)

    return get_devicetype(dxml_fullpath)


def __get_device_root(device_path):
    """Returns the root Element of the device file

    Args:
        device_path (str): full path to device file to parse

    Returns:
        xml.Element: root element of device file
    """
    if not os.path.exists(device_path):
        raise DeviceError("Could not find device: %s" % device_path)

    root = xmlhelper.get_xml_root(device_path)

    return root
