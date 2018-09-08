"""
helper module for finding installed cpu types


Author: Cameron Webb
Date: March 2018
Contact: webbjcam@gmail.com

"""

import os
import re

from tiflash.utils import xmlhelper

CPUS_DIR = "/ccs_base/common/targetdb/cpus"


class CPUError(Exception):
    """Generic CPU Error"""
    pass


def get_cpus_directory(ccs_path):
    """Returns full path to cpus directory

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        str: full path to cpus directory
    """
    cpus_directory = os.path.normpath(ccs_path + "/" + CPUS_DIR)

    if not os.path.exists(cpus_directory):
        raise CPUError("Could not find 'cpus' directory.")

    return cpus_directory


def get_cpus(ccs_path):
    """ Returns list of installed cpu names.

    Searches "<ccs_path>/ccs_base/common/targetdb/cpus" directory for
    installed cpu names.

    Args:
        ccs_path (str): full path to ccs installation to use

    Returns:
        list: cpu names

    Raises:
        CPUError: raises exception if cpus directory can not
        be found
    """
    #   Set CPU directory
    cpus_directory = get_cpus_directory(ccs_path)

    #   Get cpus xmls
    cpu_xmls = get_cpu_xmls(ccs_path, full_path=True)

    cpu_list = list()
    for cxml in cpu_xmls:
        try:    # Some xmls are not valid cpu xml files
            cpu = get_cpu_name(cxml)
        except Exception:
            continue
        cpu_list.append(cpu)

    return cpu_list


def get_cpu_xmls(ccs_path, full_path=False):
    """Gets a list of the cpu xmls files

    Args:
        ccs_path (str): path to ccs installation
        full_path (boolean, optional): returns full path of each cpu xml

    Returns:
        list: list of cpu xml files
    """
    cpu_dir = get_cpus_directory(ccs_path)
    cpus = [f for f in os.listdir(cpu_dir) if f.endswith('.xml')]

    if full_path:
        cpus = [ os.path.abspath(cpu_dir + '/' + c) for c in cpus ]

    return cpus


def get_cpu_xml_path(xml_name, ccs_path):
    """Returns full path to cpu xml if exists, else returns None.

    Args:
        xml_name (str): name of cpu to search xmls for
        ccs_path (str): path to ccs installation to use for searching xmls

    Returns:
        str or None: full path to cpu xml if exists otherwise returns None

    Raises:
        CPUError: raises exception if cpu directory can not be found
    """
    cpu_xml = None

    if not xml_name.endswith('.xml'):
        xml_name += ".xml"

    #   Set Connections directory
    cpu_xmls = get_cpu_xmls(ccs_path)

    if xml_name in cpu_xmls:
        cpu_xml = os.path.normpath(
                            get_cpus_directory(ccs_path) + "/" + xml_name)

    return cpu_xml


def get_cpu_name(xml_file):
    """ Returns full cpu name (as specified in cpuxml)

    Opens cpu xml file and reads 'id' of cpu tag.

    Args:
        xml_file (str): full path to cpu xml file to parse

    Returns:
        str: cpu name

    Raises:
        CPUError: raises exception xml is unable to be parsed

    """
    root = __get_cpu_root(xml_file)

    if root.tag != "cpu":
        raise CPUError("Error parsing cpu xml: %s" % cpu_xml)

    cpu_name = xmlhelper.get_attrib_value(root.attrib, ["desc", "id"])

    return cpu_name


def find_cpu(cpu_name, ccs_path):
    """ Returns full cpu name(s) matching 'cpu_name'

    Uses regex to try to match given 'cpu_name' to all installed
    cpu types.

    Args:
        cpu_name (str): cpu name to try to match (i.e. cortex_m4)

    Returns:
        list: list of full cpu names that matched the given
        cpu_name

    Raises:
        CPUError: raises exception if CCS installation can not be found

    """
    cpus = get_cpus(ccs_path)
    match_list = list()
    cpu_re = re.compile(cpu_name.lower())

    for c in cpus:
        if cpu_re.search(c.lower()) is not None:
            match_list.append(c)

    return match_list


def __get_cpu_root(cpu_path):
    """Returns the root Element of the cpu file

    Args:
        cpu_path (str): full path to cpu file to parse

    Returns:
        xml.Element: root element of cpu file
    """
    if not os.path.exists(cpu_path):
        raise CPUError("Could not find cpu xml: %s" % cpu_path)

    root = xmlhelper.get_xml_root(cpu_path)

    return root
