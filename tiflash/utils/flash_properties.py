"""
flash_properties.py    --   helper module for gathering device specific
                            flash property options


@author: Cameron Webb
@date: March 2018
@contact: webbjcam@gmail.com

"""

import os
import re
from xml.dom import minidom

from tiflash.utils import xmlhelper

PROPERTIES_DIR = "/ccs_base/DebugServer/propertyDB"
PROPERTIESDB_XML = "PropertiesDB.xml"

#   flashproperties translator for mapping devicetrype -> flashproperties file
FLASH_PROPERTIES_TRANSLATOR = "FlashPropertiesTranslator.xml"
FLASH_PROPERTIES_TAG = "_FlashProperties"


class FlashPropertiesError(Exception):
    """Generic FlashProperties Error"""
    pass


def __translate_to_property_xml(devicetype, translator_xml):
    """Returns property xml translated by FlashPropertiesTranslator.xml

    Args:
        ccs_path (str): full path to ccs installation to use
        devicetype (str):   devicetype

    Returns:
        str: properties.xml file to use for getting info on device
            properties (full path)

    Raises:
        FlashPropertiesError: raises exception if properties file can
            not be found
    """
    # Property File
    prop_file = None

    # Set FlashProperties Translator
    if not os.path.isfile(translator_xml):
        raise FlashPropertiesError("Could not find 'translator' file: %s" %
                                   translator_xml)

    xmldoc = minidom.parse(translator_xml)

    property_files = xmldoc.getElementsByTagName('FlashProperties')

    # Loop through device types in translator to find correct property file
    for pf in property_files:
        # only take elements that have attributes
        if pf.attributes is None or len(pf.attributes) == 0:
            continue

        property_file_name = pf.attributes['name'].value
        partnums = pf.getElementsByTagName('partnum')

        for pn in partnums:
            beginsWith = pn.attributes['beginsWith'].value

            # Prepare for regex
            beginsWithPattern = beginsWith.replace('*', '.')
            beginsWith_RE = re.compile("^" + beginsWithPattern)

            if beginsWith_RE.search(devicetype):
                prop_file = property_file_name
                break

        #   Check if we found the property file
        if prop_file is not None:
            properties_directory = os.path.dirname(translator_xml)
            if not os.path.isdir(properties_directory):
                raise FlashPropertiesError(
                    "Could not find 'properties' directory.")
            prop_file = properties_directory + "/" \
                + prop_file + FLASH_PROPERTIES_TAG + ".xml"
            prop_file = os.path.normpath(prop_file)
            if not os.path.isfile(prop_file):
                raise FlashPropertiesError("Trouble finding %s" % prop_file)
            break

    return prop_file


def get_generic_properties_xml(ccs_path):
    """Returns the flashproperty file (full path) for generic devices
    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: PropertiesDB.xml file (full path)

    Raises:
        FlashPropertiesError: raises exception if properties file can
            not be found
    """
    # Property File
    prop_file = None

    # Set Properties directory
    properties_directory = ccs_path + PROPERTIES_DIR
    if not os.path.isdir(properties_directory):
        raise FlashPropertiesError("Could not find 'properties' directory.")

    prop_file = properties_directory + '/' + PROPERTIESDB_XML

    if not os.path.isfile(prop_file):
        raise FlashPropertiesError("Could not find 'PropertiesDB' file: %s" %
                                   prop_file)

    return os.path.abspath(prop_file)



def get_device_properties_xml(devicetype, ccs_path):
    """ Returns flashproperty file (full path) for given device

    Uses the devicetype to determine the properties file

    Args:
        ccs_path (str): full path to ccs installation to use
        devicetype (str):   devicetype

    Returns:
        str: properties.xml file to use for getting info on device
            properties (full path)

    Raises:
        FlashPropertiesError: raises exception if properties file can
            not be found

    """
    # Property File
    prop_file = None

    # Set Properties directory
    properties_directory = ccs_path + PROPERTIES_DIR
    if not os.path.isdir(properties_directory):
        raise FlashPropertiesError("Could not find 'properties' directory.")

    # Try not to use Translator first
    default_file = os.path.normpath(properties_directory + "/" + devicetype +
                                    FLASH_PROPERTIES_TAG + ".xml")
    if os.path.exists(default_file):
        prop_file = default_file
    else:
        # Set FlashProperties Translator
        translator_path = properties_directory + "/" + \
            FLASH_PROPERTIES_TRANSLATOR

        if not os.path.isfile(translator_path):
            raise FlashPropertiesError("Could not find 'translator' file: %s" %
                                       FLASH_PROPERTIES_TRANSLATOR)
        prop_file = __translate_to_property_xml(devicetype, translator_path)

    if prop_file is None:
        raise FlashPropertiesError("Could not find flash property xml")

    return prop_file


def get_property_elements(xmlfile, target=None, exclude_tags=None):
    """ Returns list of properties in given xmlfile

    Opens property xml file and reads 'property' tags

    Args:
        xmlfile (str): full path to device property xml file to parse

    Returns:
        list: list of property names

    Raises:
        FlashPropertiesError: raises exception if xml is unable to be parsed

    """
    xmldoc = minidom.parse(xmlfile)

    properties = xmlhelper.get_elements_by(xmldoc, tag='property')

    if len(properties) < 1:
        raise FlashPropertiesError("Error parsing properties xml: %s"
                                   % xmlfile)

    property_elements = []
    for p in properties:
        children = xmlhelper.get_elements_by(p, tag='*')
        if len(children) != 0:
            for c in children:
                if c.tagName == 'hidden' or c.tagName == 'action':
                    break
            else:
                property_elements.append(p)

    if target is not None:
        def get_target_name(e):
            target_element = xmlhelper.get_unique_element_by(e, tag='target')
            target_name = xmlhelper.get_text_from_element(target_element)
            return target_name

        property_elements = [ p for p in property_elements if get_target_name(p) == target ]


    return property_elements


def parse_property_element(element):
    """Returns dict with parsed element information

    Args:
        element (xml.Element): property element to parse

    Returns:
        dict: dictionary of parsed element info
    """
    property_values = dict()
    property_id = xmlhelper.get_attribute_value(element, 'id')

    type_element = xmlhelper.get_unique_element_by(element, tag='valueType')
    if type_element is None:
        raise FlashPropertiesError("Invalid Property Element")

    property_values['type'] = xmlhelper.get_text_from_element(type_element)

    if property_values['type'] == 'ChoiceList':
        vals_element = xmlhelper.get_unique_element_by(element, tag='values')
        val_elements = xmlhelper.get_elements_by(vals_element, tag='value')
        property_values['choices'] = [xmlhelper.get_text_from_element(val)
                                      for val in val_elements]

    default_element = xmlhelper.get_unique_element_by(element,
                                                      tag='defaultValue')
    if default_element is not None:
        property_values['default'] = xmlhelper.get_text_from_element(
            default_element)

    return {property_id: property_values}
