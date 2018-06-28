"""
helper module for finding installed cpu types


Author: Cameron Webb
Date: March 2018
Contact: webbc92@gmail.com

"""

import os
import re
from xml.dom import minidom

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
    cpus_directory = ccs_path + CPUS_DIR
    if not os.path.isdir(cpus_directory):
        raise CPUError("Could not find 'cpus' directory.")

    #   Get cpus xmls
    cpu_xmls = list()
    for x in os.listdir(cpus_directory):
        x_fullpath = cpus_directory + "/" + x
        if os.path.isfile(x_fullpath) and x_fullpath.endswith(".xml"):
            cpu_xmls.append(x_fullpath)

    cpu_list = list()
    for cxml in cpu_xmls:
        try:    # Some xmls are not valid cpu xml files
            cpu = get_cpu_name(cxml)
        except Exception:
            continue
        cpu_list.append(cpu)

    return cpu_list


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
    xmldoc = minidom.parse(xml_file)
    cpu_element = xmlhelper.get_unique_element_by(xmldoc, 'desc', tag='cpu')
    cpu_name = xmlhelper.get_attribute_value(cpu_element, 'desc')

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
