import os
import xml.etree.ElementTree as ET

TARGETDB_DIR = "/ccs_base/common/targetdb"
PROPERTYDB_DIR = "/ccs_base/DebugServer/propertyDB"
CONNECTIONS = "/connections"
CPUS = "/cpus"
DEVICES = "/devices"


class XMLHelperError(Exception):
    """Generic XML Helper Error"""
    pass


def get_attrib_value(attribs, options, clean=True):
    """Helper for getting value from attributes.

    Pass this function the attrib dict of an element and a list of orded
    attributes to try to get the value for. If the first attrib in the list
    exists, the value of that attrib will be returned. Otherwise the next
    attrib in the list will be searched for and so on. If none of the attribs
    in the list are found, an Exception will be raised.

    Args:
        attribs (dict): dictionary of an element's attributes
        options (list): ordered list of attributes to look for
        clean (boolean): automatically clean attrib value before returning
                        (default=True)

    Returns:
        str: value of the found attribute

    Raises:
        XMLHelperError: raised if none of the attributes in the options list
                        are found
    """
    keys = attribs.keys()
    value = None

    for opt in options:
        if opt in keys:
            value = attribs[opt]
            break
    else:
        raise XMLHelperError("Could not find any of the provided attribute "
                            "options in the attributes dict.")

    if clean:
        value = clean_attrib(value)

    return value


def clean_attrib(value):
    """Cleans up value string.

    Removes any trailing '_0' that randomly show up

    Args:
        value (str): attrib value to clean

    Returns:
        str: cleaned attribute value
    """
    clean_value = value
    if value.endswith("_0"):
        clean_value = clean_value.strip('_0')

    return clean_value


def get_xml_tree(xml_path):
    """Parses xml file and returns am xml tree.

    Args:
        xml_path (str): full path to xml file to parse

    Returns:
        ElementTree.Tree: ElementTree representing xml file
    """
    if not os.path.exists(xml_path):
        raise XMLHelperError("Could not find xml file: %s" % xml_path)

    tree = ET.parse(xml_path)

    return tree


def get_xml_root(xml_path):
    """Gets the root element of the xml file.

    Args:
        xml_path (str): full path to xml file to parse

    Returns:
        ElementTree.Element: root element of xml doc
    """
    if not os.path.exists(xml_path):
        raise XMLHelperError("Could not find xml file: %s" % xml_path)

    tree = ET.parse(xml_path)
    root = tree.getroot()

    return root

def get_sibling(target_node, parent_node, index):
    """Returns the sibling node at the index relative to the target_node.

    As an example:
        target-node index = 0
        previous-sibling index = -1
        next-sibling index = 1


    Args:
        target_node (Element): reference node to get sibling node from
        parent_node (Element): parent node to target and sibling nodes
        index (int): index relative to target node (target node index = 0)

    Returns:
        Element: sibling node that
                no previous sibling node exists

    """
    # Get list of children
    children = list(parent_node)
    abs_index = children.index(target_node) + index

    return children[abs_index]



def extract_ccs_path(file_path):
    """Extracts and returns the ccs path from file path.

    Args:
        file_path (str): full path of file

    Returns:
        str: ccs path (contained in 'file_path')
    """
    file_path = file_path.replace('\\', '/')
    index = file_path.index('ccsv')
    end = file_path.index('/', index)

    ccs_path = file_path[:end]

    return ccs_path


def get_targetDB(ccs_path):
    """Provides the full path to the TargetDB in the given ccs installation.

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: returns full path to targetDB directory
    """
    if not os.path.exists(ccs_path):
        raise XMLHelperError("Could not find ccs installation: %s" % ccs_path)

    return os.path.normpath(ccs_path + '/' + TARGETDB_DIR)


def get_connections_db(ccs_path):
    """Returns path to connections folder"""
    conns_path = get_targetDB(ccs_path) + '/' + CONNECTIONS

    return os.path.normpath(conns_path)


def get_cpus_db(ccs_path):
    """Returns path to cpus folder"""
    cpus_path = get_targetDB(ccs_path) + '/' + CPUS

    return os.path.normpath(cpus_path)


def get_devices_db(ccs_path):
    """Returns path to devices folder"""
    devices_path = get_targetDB(ccs_path) + '/' + DEVICES

    return os.path.normpath(devices_path)


def get_propertyDB(ccs_path):
    """Provides the full path to the PropertyDB in the given ccs installation.

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: returns full path to propertyDB directory
    """
    if not os.path.exists(ccs_path):
        raise XMLHelperError("Could not find ccs installation: %s" % ccs_path)

    return os.path.normpath(ccs_path + '/' + PROPERTYDB_DIR)


def get_attribute_value(element, attribute):
    """Returns value of element's 'attribute'

    Args:
        element (xml.Element): xml.Element object to check
        attribute (str): attribute name to get

    Returns:
        str: returns attribute value
    """
    value = None

    if element.hasAttribute(attribute):
        value = element.attributes[attribute].value

    return value


def get_elements_by(xmldoc, *args, **kwargs):
    """Searches xml for nodes with provided tag, attributes (args) and
    attribute key-val pairs (kwargs)

    Args:
        xmldoc (xml.dom.minidom): minidom object (returned by minidom.parse())
        tag (str, optional): name of tag to search for
        *args (str, optional): attribute names to check element has
        **kwargs (str=str, optional): attributeName=attributeValue to check
            element has
    Returns:
        list: returns list of xml.Elements that have given tag, attribute(s)
        and/or attribute key-val(s)
    """
    if 'tag' in kwargs.keys():
        tag = kwargs.pop('tag')
    else:
        tag = None

    if tag is None:  # Get all elements
        tag = '*'
    elements = xmldoc.getElementsByTagName(tag)

    if len(args):
        for a in args:
            elements = [e for e in elements if e.hasAttribute(a)]

    if len(kwargs):
        for k in kwargs.keys():
            elements = [e for e in elements if e.hasAttribute(k) and
                        e.attributes[k].value == kwargs[k]]

    return elements


def get_unique_element_by(xmldoc, *args, **kwargs):
    """Searches xml for nodes with provided tag, attributes (args) and
    attribute key-val pairs (kwargs). Returns the first element found.

    Performs 'get_elements_by()' and returns first element

    Args:
        xmldoc (xml.dom.minidom): minidom object (returned by minidom.parse())
        tag (str, optional): name of tag to search for
        *args (str, optional): attribute names to check element has
        **kwargs (str=str, optional): attributeName=attributeValue to check
            element has
    Returns:
        list: returns xml.Element that has given tag, attribute(s)
        and/or attribute key-val(s)
    """
    if 'tag' in kwargs.keys():
        tag = kwargs.pop('tag')
    else:
        tag = None

    elements = get_elements_by(xmldoc, *args, tag=tag, **kwargs)
    unique_element = None

    if len(elements) > 0:
        unique_element = elements[0]

    return unique_element


def get_text_from_element(element):
    """Returns the text value of an element

    Args:
        element (xml.Element): element to parse and retrieve text value
    """
    text_elements = []
    if element.hasChildNodes():
        children = element.childNodes
        text_elements = [te for te in children if te.nodeName == '#text']

    if len(text_elements) == 0:
        #raise XMLHelperError("Could not find text from given element")
        text = ''
    else:
        text = text_elements[0].nodeValue

    return text
