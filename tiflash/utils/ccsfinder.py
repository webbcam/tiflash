"""
helper module for finding CCS install paths


Author: Cameron Webb
Date: March 2018
Contact: webbc92@gmail.com

"""
import platform
import os.path as path
import os
import re


TI_DIRECTORY = "ti"


class FindCCSError(Exception):
    """Generic FindCCS Error"""
    pass


def find_ccs(version=None):
    """ Finds CCS installation path.

    Searches (OS specific) default installation paths for CCS. If no version
    is provided, will return the latest version installed.

    Args:
        version (int, optional): version number of CCS to look for

    Returns:
        str: path to CCS installation

    Raises:
        FindCCSError: raises exception if CCS installation can not be found

    """
    ccs_directory = ""
    system = platform.system()
    if system == "Windows":
        WINDOWS_CCS_PATH = os.environ['HOMEDRIVE']
        ccs_directory = WINDOWS_CCS_PATH
    elif system == "Linux":
        LINUX_CCS_PATH = os.environ['HOME']
        ccs_directory = LINUX_CCS_PATH
    elif system == "Darwin":
        MAC_CCS_PATH = "/Applications"
        ccs_directory = MAC_CCS_PATH
    else:
        raise FindCCSError("Unsupported Operating System: %s" % system)

    ccs_directory = os.path.normpath(ccs_directory + '/' + TI_DIRECTORY)

    # Ensure ccs_directory exists
    if not path.exists(ccs_directory):
        raise FindCCSError("%s does not exist" % ccs_directory)

    # Find latest or specific CCS version
    directories = [d for d in os.listdir(ccs_directory)
                   if path.isdir(ccs_directory + "/" + d)]
    ccs_pattern = "ccsv(\d+)"
    ccs_re = re.compile(ccs_pattern)
    ccs_installations = [ccs for ccs in directories
                         if ccs_re.match(ccs) is not None]

    # Check if any CCS installations were found
    if len(ccs_installations) == 0:
        raise FindCCSError(
            "Could not find any installations of Code Composer Studio")

    # Returns version number as an int for comparison
    def get_version(ccs_name):
        m = ccs_re.match(ccs_name)
        return int(m.group(1)) if m is not None else None

    if version is not None:  # Get specific CCS Installation
        for ccs_name in ccs_installations:
            if get_version(ccs_name) == version:
                ccs_install = ccs_name
                break
        else:
            raise FindCCSError("Could not find installation for CCSv%d"
                               % version)
    else:   # Get Latest CCS Installation
        ccs_install = max(ccs_installations, key=get_version)

    return path.abspath(ccs_directory + "/" + ccs_install)
