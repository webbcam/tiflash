"""
ccxml.py    --   helper module for modifying a ccxml file


@author: Cameron Webb
@date: March 2018
@contact: webbc92@gmail.com

"""

import platform
import os
from xml.dom import minidom

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
        os.mkdir(ccxml_dir)

    return ccxml_dir


def get_serno_from_ccxml(ccxml_path):
    """Returns the serno from the ccxml file

    Args:
        ccxml_path (str): full path to ccxml file to parse

    Returns:
        str: serial number set in ccxml file
    """
    xmldoc = minidom.parse(ccxml_path)

    try:
        debugprobe_property = xmlhelper.get_unique_element_by(
            xmldoc, tag='property', id='Debug Probe Selection')
    except Exception:
        raise CCXMLError("""%s does not support Debug Probe Selection
            """ % ccxml_path)

    serno_property = xmlhelper.get_unique_element_by(debugprobe_property,
                                                     tag='property')

    serno = xmlhelper.get_attribute_value(serno_property, 'Value')

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

    # Add serno property to ccxml file
    ccxml_doc = minidom.parse(ccxml_path)
    connection_element = xmlhelper.get_unique_element_by(ccxml_doc,
                                                         tag='connection')
    platform_element = xmlhelper.get_unique_element_by(ccxml_doc,
                                                       tag='platform')

    connection_element.insertBefore(serno_property, platform_element)

    ccxml_doc.writexml(open(ccxml_path, 'w'))

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
    xmldoc = minidom.parse(conn_xml)

    try:
        serno_property = xmlhelper.get_unique_element_by(
            xmldoc, tag='property', ID='SEPK.POD_PORT')
    except Exception:
        raise CCXMLError("""This connection does support
            Serial Number specification""")

    serno_property.setAttribute('id', serno_property.attributes['Name'].value)
    serno_property.removeAttribute('Name')

    if serno_property.hasAttribute('desc'):
        serno_property.removeAttribute('desc')

    serno_property.setAttribute('Value', '1')

    serno_property.removeAttribute('ID')

    serno_choice = xmlhelper.get_unique_element_by(
        serno_property, tag='choice', Name='Select by serial number')

    prop = xmlhelper.get_unique_element_by(serno_choice, tag='property',
                                           ID='SEPK.POD_SERIAL')

    prop.setAttribute('Value', serno)
    prop.setAttribute('id', prop.getAttribute('Name'))
    prop.removeAttribute('ID')
    prop.removeAttribute('Name')

    choice_list = xmlhelper.get_elements_by(serno_property, tag='choice')

    # Remove any extra choices
    for choice in choice_list:
        if choice is not serno_choice:
            serno_property.removeChild(choice)

    return serno_property


def get_connection_xml(ccxml_path, ccs_path):
    """Returns the full path to the connection xml specified in the ccxml.

    Args:
        ccxml_path (str): full path to ccxml file to modify
        ccs_path (str): full path to ccs installation to use

    Returns:
        (str) path to connection xml
    """
    xmldoc = minidom.parse(ccxml_path)
    xmlpath = None

    try:
        connection_element = xmlhelper.get_unique_element_by(
            xmldoc, 'xml', tag='instance', xmlpath='connections')
    except Exception:
        raise CCXMLError("Could not find connection xml from given ccxml file")

    xmlname = xmlhelper.get_attribute_value(connection_element, 'xml')
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
    xmldoc = minidom.parse(ccxml_path)
    xmlpath = None

    try:
        device_element = xmlhelper.get_unique_element_by(
            xmldoc, 'xml', tag='instance', xmlpath='devices')
    except Exception:
        raise CCXMLError("Could not find device xml from given ccxml file")

    xmlname = xmlhelper.get_attribute_value(device_element, 'xml')
    xmlpath = get_devices_directory(ccs_path) + '/' + xmlname
    xmlpath = os.path.normpath(xmlpath)

    return xmlpath


def get_ccxmls():
    """Gets a list of the target configurations (ccxml files)

    Returns:
        list: list of target configurations (ccxml files)
    """
    ccxml_dir = get_ccxml_directory()
    ccxmls = [f for f in os.listdir(ccxml_dir) if f.endswith('.ccxml')]

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
