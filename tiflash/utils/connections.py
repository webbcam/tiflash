"""
helper module for finding installed connection types


Author: Cameron Webb
Date: March 2018
Contact: webbc92@gmail.com

"""

import os
import re
from xml.dom import minidom

from tiflash.utils import xmlhelper

CONNECTIONS_DIR = "/ccs_base/common/targetdb/connections"


class ConnectionsError(Exception):
    """Generic Connection Error"""
    pass


def get_connections_directory(ccs_path):
    """Returns full path to connections directory

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: full path to connections directory
    """
    connections_directory = os.path.normpath(ccs_path + "/" + CONNECTIONS_DIR)

    if not os.path.exists(connections_directory):
        raise ConnectionsError("Could not find 'connections' directory.")

    return connections_directory


def get_connections(ccs_path):
    """ Returns list of installed connection names.

    Searches "<ccs_path>/ccs_base/common/targetdb/connections" directory for
    installed connection names.

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        list: connection names

    Raises:
        ConnectionsError: raises exception if connections directory can not
            be found

    """
    #   Set Connections directory
    connections_directory = get_connections_directory(ccs_path)

    #   Get connections xmls
    connection_xmls = list()
    for x in os.listdir(connections_directory):
        x_fullpath = connections_directory + "/" + x
        if os.path.isfile(x_fullpath) and x_fullpath.endswith(".xml"):
            connection_xmls.append(x_fullpath)

    connection_list = list()
    for cxml in connection_xmls:
        try:    # Some xmls are not valid connection xml files
            connection = get_connection_name(cxml)
        except Exception:
            continue
        connection_list.append(connection)

    return connection_list


# TODO: Not implemented
def get_connection_xml(xml_name, ccs_path):
    """Returns full path to connection xml if exists, else returns None.

    Args:
        xml_name (str): name of connection to search xmls for (i.e. TIXDS110)
        ccs_path (str): path to ccs installation to use for searching xmls

    Returns:
        str or None: full path to connection xml if exists
            otherwise returns None

    Raises:
        ConnectionsError: raises exception if connections directory can not
            be found
    """
    connection_xml = None

    if not xml_name.endswith('.xml'):
        xml_name += ".xml"

    #   Set Connections directory
    connections_directory = ccs_path + CONNECTIONS_DIR
    if not os.path.isdir(connections_directory):
        raise ConnectionsError("Could not find 'connections' directory.")

    return connection_xml


def get_connection_name(xmlfile):
    """ Returns full connection name (as specified in connectionxml)

    Opens connection xml file and reads 'desc' of connection tag.

    Args:
        xmlfile (str): full path to connection xml file to parse

    Returns:
        str: connection name

    Raises:
        ConnectionsError: raises exception xml is unable to be parsed

    """
    xmldoc = minidom.parse(xmlfile)
    connection_element = xmlhelper.get_unique_element_by(xmldoc,
                                                    'desc', tag='connection')
    connection_name = xmlhelper.get_attribute_value(connection_element, 'desc')

    return connection_name


def find_connection(connection_name, ccs_path):
    """ Returns full connection name(s) matching 'connection_name'

    Uses regex to try to match given 'connection_name' to all installed
    connection types.

    Args:
        connection_name (str): connection name to try to match (i.e. xds110)

    Returns:
        list: list of full connection names that matched the given
        connection_name

    Raises:
        ConnectionsError: raises exception if CCS installation can not be found

    """
    connections = get_connections(ccs_path)
    match_list = list()
    connection_re = re.compile(connection_name.lower())

    for c in connections:
        if connection_re.search(c.lower()) is not None:
            match_list.append(c)

    return match_list
