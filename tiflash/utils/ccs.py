"""
helper module for CCS specifc functions


Author: Cameron Webb
Date: March 2018
Contact: webbjcam@gmail.com

"""

import platform
import os
import re

TI_DIRECTORY = "ti"
DEFAULT_WORKSPACE = "@user.home/.tiflash/workspace"

class FindCCSError(Exception):
    """Generic FindCCS Error"""
    pass

def get_ccs_prefix():
    """Returns full path to directory containing ccs installations.

    This can be the default directory or a custom one (set by CCS_PREFIX
    environment variable)

    Returns:
        str: full path to directory containing ccs installations
    """
    try:    # Custom CCS Installation path
        ccs_prefix = os.environ['CCS_PREFIX']

    except KeyError:    # Default CCS Installation paths
        system = platform.system()
        if system == "Windows":
            WINDOWS_CCS_PATH = os.environ['HOMEDRIVE']
            ccs_prefix = WINDOWS_CCS_PATH
        elif system == "Linux":
            LINUX_CCS_PATH = os.environ['HOME']
            ccs_prefix = LINUX_CCS_PATH
        elif system == "Darwin":
            MAC_CCS_PATH = "/Applications"
            ccs_prefix = MAC_CCS_PATH
        else:
            raise FindCCSError("Unsupported Operating System: %s" % system)

        ccs_prefix = os.path.normpath(ccs_prefix + '/' + TI_DIRECTORY)

    # Ensure ccs_directory exists
    if not os.path.exists(ccs_prefix):
        raise FindCCSError("Could not a find CCS Installation directory")

    return ccs_prefix

def __get_ccs_exe_name():
    """Returns the name of the ccstudio executable according to OS.

    Returns:
        str: name of ccstudio executable for current OS
    Raises:
        Exception: raised if OS not supported
    """
    system = platform.system()
    ccs_exe = None

    if system == "Windows":
        ccs_exe = "eclipsec.exe"
    elif system == "Linux":
        ccs_exe = "ccstudio"
    elif system == "Darwin":
        ccs_exe = "ccstudio"
    else:
        raise Exception("Unsupported Operating System: %s" % system)

    return ccs_exe

def __get_ccs_exe_path():
    """Returns the path of ccstudio executable relative to the ccs-root directory

    Returns:
        str: path to ccstudio executable for current OS
    Raises:
        Exception: raised if OS not supported
    """
    ccs_exe = __get_ccs_exe_name()
    system = platform.system()
    ccs_exe_path = None

    if system == "Windows":
        ccs_exe_path = "eclipse/%s" % ccs_exe
    elif system == "Linux":
        ccs_exe_path = "eclipse/%s" % ccs_exe
    elif system == "Darwin":
        ccs_exe_path = "eclipse/Ccstudio.app/Contents/MacOS/%s" % ccs_exe
    else:
        raise Exception("Unsupported Operating System: %s" % system)

    return ccs_exe_path


def __is_ccs_root(path):
    """Returns True or False depending if path is a valid "ccs-root" folder.

    A valid "ccs-root" folder contains the following:
        1. eclipse/[ccstudio or eclipsec.exe]
        2. eclipse/ccs.properties
        3. ccs_base/

    Args:
        path (str): full path to check
    Returns:
        boolean: True if valid; False if invalid
    Raises:
        OSError: raised if path does not exist
    """
    ccs_exe = __get_ccs_exe_path()
    directories = [ directory for directory in os.listdir(path)
                    if os.path.isdir(path + '/' + directory) ]

    # 0. Check for eclipse folder
    if "eclipse" not in directories:
        return False

    # 1. Check for ccs.properties file
    if not os.path.exists(path + "/eclipse/ccs.properties"):
        return False

    # 2. Check for ccs executable
    if not os.path.exists(path + '/' + ccs_exe):
        return False

    # 3. Check for ccs_base directory
    if "ccs_base" not in directories:
        return False

    return True

def get_ccs_pf_filters(ccs_root):
    """Returns list of PF Filters installed with passed ccs installation

    Args:
        ccs_root (str): full path to root of ccs installation

    Returns:
        list: list of PF Filters (strings) installed in ccs installation
    """
    pf_filters = list()
    with open(ccs_root + '/eclipse/ccs.properties') as f:
        lines = f.readlines()
        for line in lines:
            match = re.match("^PF_FILTERS=([a-zA-Z0-9\,]*)", line, flags=re.IGNORECASE)
            if match:
                pf_filters = match.group(1).split(',')
                break
    return pf_filters

def get_ccs_version(ccs_root):
    """Returns the version number of the ccs installation

    Version number is as found in ccs.properties file

    Args:
        ccs_root (str): full path to root of ccs installation
    Returns:
        str: full version/build id as found in ccs.properties file
    Raises:
        OSError: raised if ccs.properties file cannot be found
    """
    version = None
    with open(ccs_root + '/eclipse/ccs.properties') as f:
        lines = f.readlines()
        for line in lines:
            match = re.match("^ccs_buildid=([0-9]+.[0-9]+.[0-9]+.[0-9]+)", line, flags=re.IGNORECASE)
            if match:
                version = match.group(1)
                break
    return version

def get_ccs_installations(ccs_prefix):
    """Returns a list of paths to all found ccs-root locations.

    Uses ccs_prefix to begin search.

    Args:
        ccs_prefix (str): path to top level directory containing ccs
            installations
    Returns:
        list: list of paths to ccs installations found in search
    Raises:
        OSError: raised if ccs_prefix does not exist
    """
    ccs_installations = []

    def dfw_search(path):
        paths = []
        if __is_ccs_root(path):
            paths.append(path)
        else:
            directories = [ directory for directory in os.listdir(path)
                            if os.path.isdir(path + '/' + directory) ]

            ccs_directories = [ ccs_directory for ccs_directory in directories
                                if re.search("^ccs", ccs_directory, flags=re.IGNORECASE) ]

            for ccs_dir in ccs_directories:
                paths.extend(dfw_search(path + '/' + ccs_dir))

        return paths

    return dfw_search(ccs_prefix)


def get_workspace_dir():
    """Returns the workspace directory to use for tiflash.

    Returns:
        str: workspace to use for tiflash (fullpath)
    """
    # Uses user's home directory
    workspace = DEFAULT_WORKSPACE

    return workspace


def find_ccs(version=None, ccs_prefix=None):
    """ Finds CCS installation path.

    Searches (OS specific) default installation paths for CCS. If no version
    is provided, will return the latest version installed.
    Will return the latest version that matches the specified version number.
    e.g. if version='8' and both 8.1 and 8.2 are installed, the path to 8.2
    will be returned.

    Args:
        version (str, optional): version number of CCS to look for
        ccs_prefix (str, optional): path to CCS_PREFIX (uses default/env variable if not provided)

    Returns:
        str: path to CCS root installation

    Raises:
        FindCCSError: raises exception if CCS installation can not be found

    """
    ccs_installation_versions = dict()
    version_list = list()

    # Get default ccs_prefix if none provided
    if ccs_prefix is None:
        ccs_prefix = get_ccs_prefix()

    # Get all CCS installations
    ccs_installations = get_ccs_installations(ccs_prefix)

    # Check if any CCS installations were found
    if len(ccs_installations) == 0:
        raise FindCCSError(
            "Could not find any installations of Code Composer Studio")

    # Get version numbers of installations
    for installation in ccs_installations:
        try:
            v = get_ccs_version(installation)
            ccs_installation_versions[v] = installation     # duplicate versions will be overwritten
            version_list.append(v)
        except:
            continue

    # Filter to only matching version numbers
    if version is not None:
        version_list = [ v for v in version_list if re.search("^" + version, v) ]

        # Raise error if specific version could not be found
        if len(version_list) == 0:
            raise FindCCSError("Could not find installation for CCS version: %s" % version)

    ccs_path = ccs_installation_versions[max(version_list)]
    return os.path.normpath(ccs_path)
