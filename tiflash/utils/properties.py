"""
helper module for finding device specific properties


Author: Cameron Webb
Date: March 2018
Contact: webbc92@gmail.com

"""

from xml.dom import minidom


class PropertiesError(Exception):
    """Generic Device Properties Error"""
    pass


def get_elements_by(xmlpath, tag=None, *args, **kwargs):
    """Searches xml for nodes with provided tag, attributes (args) and
    attribute key-val pairs (kwargs)

    Args:
        xml_path (str): path to xml file to parse
        tag (str, optional): name of tag to search for
        *args (str, optional): attribute names to check element has
        **kwargs (str=str, optional): attributeName=attributeValue to check
            element has
    Returns:
        list: returns list of xml.Elements that have given tag, attribute(s)
        and/or attribute key-val(s)
    """
    xmldoc = minidom.parse(xmlpath)
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


def get_property_by_id(xml_path, property_id):
    """Searches the property nodes in the xml for the given id, returns the
    value of the first matching node.

    Args:
        xml_path (str): the full path to the xml doc to search

    Returns:
        str or None: the value attribute of the property with the given id or
            None if specified property could not be found

    Raises:
        PropertiesError: raises exception if xml_name does not exist
    """
    valid_properties = get_elements_by(xml_path, tag='property',
                                       id=property_id)
    if len(valid_properties) < 1:
        raise PropertiesError("Could find property with id: %s" % property_id)
    elif len(valid_properties) != 1:
        raise PropertiesError("Found too many properties with id: %s"
                              % property_id)

    value = valid_properties[0].attributes['Value'].value

    return value
