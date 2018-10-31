"""
ccxml.py    --   helper module for modifying a ccxml file


@author: Cameron Webb
@date: March 2018
@contact: webbjcam@gmail.com

"""

import platform
import os
#import xml.etree.ElementTree as ET

from tiflash.utils.connections import get_connections_directory
from tiflash.utils.devices import get_devices_directory
from tiflash.utils import xmlhelper

TARGET_CONFIG_EXT = "ti/CCSTargetConfigurations"


class CCXMLError(Exception):
    """Generic CCXML Error"""
    pass


def get_ccxml_directory():
    system = platform.system()
    if system == "Windows":
        WINDOWS_TARGET_CONFIGS_PATH = \
            os.environ['USERPROFILE'] + '/' + TARGET_CONFIG_EXT
        ccxml_directory = WINDOWS_TARGET_CONFIGS_PATH
    elif system == "Linux" or system == "Darwin":
        UNIX_TARGET_CONFIGS_PATH = os.environ['HOME'] + '/' + TARGET_CONFIG_EXT
        ccxml_directory = UNIX_TARGET_CONFIGS_PATH
    else:
        raise CCXMLError("Unsupported Operating System: %s" % system)

    ccxml_dir =  os.path.normpath(ccxml_directory)
    if not os.path.isdir(ccxml_dir):
        os.makedirs(ccxml_dir)

    return ccxml_dir


def get_devicetype(ccxml_path):
    """Returns the devicetype from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file to parse

    Returns:
        str: devicetype set in ccxml file
    """
    devicetype = None
    root = __get_ccxml_root(ccxml_path)

    instance = root.find("configuration/connection/platform/instance")

    if instance is None:
        raise CCXMLError("Error parsing devicetype from ccxml.")

    devicetype = xmlhelper.get_attrib_value(instance.attrib, ["desc", "id"])

    return devicetype


def get_connection(ccxml_path):
    """Returns the connection from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file to parse

    Returns:
        str: connection set in ccxml file
    """
    connection = None
    root = __get_ccxml_root(ccxml_path)

    instance = root.find("configuration/connection")

    if instance is None:
        raise CCXMLError("Error parsing connection from ccxml.")

    connection = xmlhelper.get_attrib_value(instance.attrib, ["id"])

    return connection



def get_serno(ccxml_path):
    """Returns the serno from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file to parse

    Returns:
        str: serial number set in ccxml file
    """
    serno = None
    root = __get_ccxml_root(ccxml_path)

    instance = root.find("configuration/connection/"
                            "property[@id='Debug Probe Selection']/"
                            "choice[@Name='Select by serial number']/property")

    if instance is None:
        raise CCXMLError("%s does not support Debug Probe Selection"
                            % ccxml_path)

    serno = xmlhelper.get_attrib_value(instance.attrib, ["Value"])

    return serno


def add_serno(ccxml_path, serno, ccs_path):
    """Adds the given serial number to the ccxml file.

    Args:
        ccxml_path (str): full path to ccxml file to modify
        serno (str): serial number of device to add to ccxml file
        ccs_path (str): full path to ccs installation to use
    """
    conn_xml = get_connection_xml(ccxml_path, ccs_path)

    # Get Serial Number Element from Connection XML File
    serno_property = _create_serno_property(serno, conn_xml)

    tree = xmlhelper.get_xml_tree(ccxml_path)
    root = tree.getroot()

    connection_element = root.find("configuration/connection")
    platform_element = connection_element.find("platform[last()]")

    # Get index of where to insert serno property
    children = list(connection_element)     # Get list of children
    serno_index = children.index(platform_element)

    # Insert serno property
    connection_element.insert(serno_index, serno_property)

    # Update ccxml file
    tree.write(ccxml_path, encoding='utf-8', xml_declaration=True)

    return True


def _create_serno_property(serno, conn_xml):
    """INTERNAL FUNCTION: Creates a serial number property from the given
        connection xml file and adds the given serial number.

    Args:
        serno (str): serial number of device to use
        conn_xml (str): path to device specific connection xml (this can be
            retrieved by 'get_connection_xml()'

    Returns:
        xml.Element: an xml.Element representing the serial number property to
            be added to an xml tree
    """

    tree = xmlhelper.get_xml_tree(conn_xml)
    root = tree.getroot()

    debugprobe_property = root.find("property[@Name='Debug Probe Selection']")

    if debugprobe_property is None:
        raise CCXMLError("This connection does support "
                        "Serial Number specification")

    debugprobe_property.attrib['id'] = debugprobe_property.attrib.pop('Name')

    debugprobe_property.attrib.pop('desc', None)

    debugprobe_property.attrib['Value'] = '1'

    debugprobe_property.attrib.pop('ID')

    serno_property = debugprobe_property.find(
        "choice[@Name='Select by serial number']"
        "/property[@ID='SEPK.POD_SERIAL']")

    serno_property.attrib['Value'] = serno
    serno_property.attrib['id'] = serno_property.attrib.pop('Name')
    serno_property.attrib.pop('ID')

    serno_choice = debugprobe_property.find(
                        "choice[@Name='Select by serial number']")

    choices = list(debugprobe_property)     # Get list of children
    for choice in choices:
        if choice != serno_choice:
            debugprobe_property.remove(choice)

    return debugprobe_property


def get_connection_xml(ccxml_path, ccs_path):
    """Returns the full path to the connection xml specified in the ccxml.

    Args:
        ccxml_path (str): full path to ccxml file to modify
        ccs_path (str): full path to ccs installation to use

    Returns:
        (str) path to connection xml
    """
    root = xmlhelper.get_xml_root(ccxml_path)
    xmlpath = None

    connection_name = get_connection(ccxml_path)
    connection_instance = root.find("configuration/instance[@id='%s']"
                                    % connection_name)
    conn_element = root.find("configuration/connection")
    p_conn_element = root.find("configuration/connection/..")

    conn_instance = xmlhelper.get_sibling(conn_element, p_conn_element, -1)
    if conn_instance is None:
        raise CCXMLError("Could not find connection xml from given ccxml file")

    xmlname = conn_instance.attrib['xml']

    xmlpath = get_connections_directory(ccs_path) + '/' + xmlname
    xmlpath = os.path.normpath(xmlpath)

    return xmlpath


def get_device_xml(ccxml_path, ccs_path):
    """Returns the full path to the device xml specified in the ccxml.

    Args:
        ccxml_path (str): full path to ccxml file to modify
        ccs_path (str): full path to ccs installation to use

    Returns:
        (str) path to device xml
    """
    root = xmlhelper.get_xml_root(ccxml_path)
    xmlpath = None

    device_instance = root.find("configuration/connection/platform/instance[@xml]")
    if device_instance is None:
        raise CCXMLError("Could not find device xml from given ccxml file")

    xmlname = device_instance.attrib['xml']

    xmlpath = get_devices_directory(ccs_path) + '/' + xmlname
    xmlpath = os.path.normpath(xmlpath)

    return xmlpath


def get_ccxmls(full_path=False):
    """Gets a list of the target configurations (ccxml files)

    Args:
        full_path (boolean, optional): returns full path of each ccxml

    Returns:
        list: list of target configurations (ccxml files)
    """
    ccxml_dir = get_ccxml_directory()
    ccxmls = [f for f in os.listdir(ccxml_dir) if f.endswith('.ccxml')]

    if full_path:
        ccxmls = [ os.path.abspath(ccxml_dir + '/' + c) for c in ccxmls ]


    return ccxmls


def get_ccxml_path(ccxml_name):
    """Checks if ccxml file exists and returns full path if it does.

    Args:
        name (str): name of ccxml file (does not have to include '.ccxml'
            extension)

    Returns:
        str, None: full path to ccxml file if it exists, else None
    """
    ccxml_path = None
    if not ccxml_name.endswith(".ccxml"):
        ccxml_name += ".ccxml"

    existing_ccxmls = get_ccxmls()
    if ccxml_name in existing_ccxmls:
        ccxml_path = os.path.normpath(get_ccxml_directory() + "/" + ccxml_name)

    return ccxml_path


def __get_ccxml_root(ccxml_path):
    """Returns the root Element of the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file to parse

    Returns:
        xml.Element: root element of ccxml file
    """
    if not os.path.exists(ccxml_path):
        raise CCXMLError("Could not find ccxml: %s" % ccxml_path)

    root = xmlhelper.get_xml_root(ccxml_path)

    return root
