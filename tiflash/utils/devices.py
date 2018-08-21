"""
helper module for finding installed device types


Author: Cameron Webb
Date: March 2018
Contact: webbc92@gmail.com

"""

import os
import re
import json
from xml.dom import minidom

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


def get_cpu_xml(device_xml, ccs_path):
    """Returns the full path to cpu xml specified in given device xml

    Args:
        device_xml (str): full path to device xml to parse

    Returns:
        str: full path to cpu xml
    """
    if not os.path.exists(device_xml):
        raise DeviceError("Cannot find '%s' "
                          "Please install drivers for this device."
                          % device_xml)

    xmldoc = minidom.parse(device_xml)

    try:
        cpu = xmlhelper.get_unique_element_by(xmldoc, tag='instance',
                                              xmlpath='cpus')
        cpu_xml = xmlhelper.get_attribute_value(cpu, 'xml')
        cpu_xml = os.path.normpath(
            get_cpus_directory(ccs_path) + '/' + cpu_xml)

    except xmlhelper.XMLHelperError:
        cpu_xml = None

    return cpu_xml


def get_default_connection_xml(device_xml, ccs_path):
    """Returns the full path to connection xml specified in given device xml
    by 'DefaultConnection'

    Args:
        device_xml (str): full path to device xml to parse

    Returns:
        str: full path to connection xml
    """
    if not os.path.exists(device_xml):
        raise DeviceError("Cannot find '%s' "
                          "Please install drivers for this device."
                          % device_xml)

    xmldoc = minidom.parse(device_xml)

    try:
        connection = xmlhelper.get_unique_element_by(xmldoc, tag='property',
                                                     id='DefaultConnection')
        connection_xml = xmlhelper.get_attribute_value(connection, 'Value')
        connection_xml = os.path.normpath(get_connections_directory(ccs_path) +
                                          '/' + connection_xml)
    except xmlhelper.XMLHelperError:
        raise DeviceError("Could not retrieve default connection xml from: %s"
                          % device_xml)

    return connection_xml


def get_devices(ccs_path):
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
    device_xmls = list()
    for x in os.listdir(devices_directory):
        x_fullpath = devices_directory + "/" + x
        if os.path.isfile(x_fullpath) and x_fullpath.endswith(".xml"):
            device_xmls.append(x_fullpath)

    device_list = list()
    for cxml in device_xmls:
        try:    # Some xmls are not valid device xml files
            device = get_device_name(cxml)
        except Exception:
            continue
        device_list.append(device)

    return device_list


def get_device_xml(device_name, ccs_path):
    """Returns full path to device xml if exists, else returns None.

    Args:
        device_name (str): name of device to search xmls for
        ccs_path (str): path to ccs installation to use for searching xmls

    Returns:
        str or None: full path to device xml if exists, otherwise returns None

    Raises:
        DeviceError: raises exception if devices directory can not
            be found
    """
    device_xml = None

    #   Set Devices directory
    devices_directory = get_devices_directory(ccs_path)

    # Get devices xmls
    device_xmls = list()
    for x in os.listdir(devices_directory):
        x_fullpath = devices_directory + "/" + x
        if os.path.isfile(x_fullpath) and x_fullpath.endswith(".xml"):
            device_xmls.append(x_fullpath)

    for dxml in device_xmls:
        try:    # Some xmls are not valid device xml files
            device = get_device_name(dxml)
        except Exception:
            continue

        if device == device_name.upper():
            device_xml = os.path.normpath(dxml)
            break

    else:
        raise DeviceError("""Could not find device xml for %s. Please install
            drivers for %s.""" % (device_name, device_name))

    return device_xml


def get_device_name(xmlfile):
    """ Returns full device name (as specified in devicexml)

    Opens device xml file and reads 'desc' of device tag.

    Args:
        xmlfile (str): full path to device xml file to parse

    Returns:
        str: device name

    Raises:
        DeviceError: raises exception xml is unable to be parsed

    """
    xmldoc = minidom.parse(xmlfile)
    device_element = xmlhelper.get_unique_element_by(
        xmldoc, 'partnum', tag='device')

    device_name = xmlhelper.get_attribute_value(device_element, 'partnum')

    return device_name


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
    devices = get_devices(ccs_path)
    match_list = list()
    device_re = re.compile(device_name.lower())

    for d in devices:
        if device_re.search(d.lower()) is not None:
            match_list.append(d)

    return match_list


def get_device_xml_by_serno(serno, ccs_path):
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
    devices_directory = ccs_path + DEVICES_DIR
    if not os.path.isdir(devices_directory):
        raise DeviceError("Could not find 'devices' directory.")

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

        dxml_fullpath = devices_directory + "/" + dxml
        if not os.path.isfile(dxml_fullpath):
            raise DeviceError("Could not find '%s' file." % dxml)

        return dxml_fullpath


def get_device_by_serno(serno, ccs_path):
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
    dxml_fullpath = get_device_xml_by_serno(serno, ccs_path)

    return get_device_name(dxml_fullpath)
