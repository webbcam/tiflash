import os

TARGETDB_DIR = "/ccs_base/common/targetdb"
PROPERTYDB_DIR = "/ccs_basse/DebugServer/propertyDB"
CONNECTIONS = "/connections"
CPUS = "/cpus"
DEVICES = "/devices"


class XMLHelperError(Exception):
    """Generic XML Helper Error"""
    pass


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
