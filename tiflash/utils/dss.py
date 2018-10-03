"""
helper module for calling Debug Server Scripting (dss)


Author: Cameron Webb
Date: March 2018
Contact: webbjcam@gmail.com

"""

import subprocess
import platform
import os

from tiflash.utils.result import ResultServer

MAIN_JS_PATH = "js/main.js"
ECLIPSE_SUBPATH = "/eclipse"
DSS_ARGS = ['-nosplash', '-application', 'com.ti.ccstudio.apps.runScript',
            '-product', 'com.ti.ccstudio.branding.product', '-dss.rhinoArgs']

CMD_DEFAULT_TIMEOUT = 60

class DSSError(Exception):
    """Generic DSS Error"""
    pass


def find_dss(ccs_path):
    """Finds path to eclipsec/ccstudio executable.

    Searches (OS specific) CCS installation directory for eclipsec/ccstudio
    executable.

    Args:
        ccs_path (str): path to ccs installation to use

    Returns:
        str: path to eclipsec/ccstudio exe

    Raises:
        DSSError: raises exception if can not find DSS script launcher

    """
    system = platform.system()
    script_launcher = None
    script_launcher_path = None

    if system == "Windows":
        script_launcher = "eclipsec.exe"
    elif system == "Linux":
        script_launcher = "ccstudio"
    elif system == "Darwin":
        script_launcher = "ccstudio"
    else:
        raise DSSError("Unsupported Operating System: %s" % system)

    if not os.path.exists(ccs_path):
        raise DSSError("Could not find CCS installation: %s" % ccs_path)

    walker = os.walk(ccs_path + ECLIPSE_SUBPATH)

    for root, dirs, files in walker:
        if script_launcher in files:
            script_launcher_path = os.path.join(root, script_launcher)
            script_launcher_path = os.path.normpath(script_launcher_path)
            break

    else:
        raise DSSError("Could not find script launcher: %s" % script_launcher)

    return script_launcher_path


def call_dss(dss_path, commands, workspace=None, timeout=CMD_DEFAULT_TIMEOUT):
    """Calls js/main.js via new script runner (eclipsec)

    Makes a subprocess call to main.js by using the given eclipsec exe

    Args:
        dss_path (str): Path to dss.bat/.sh installation to use
        commands (list): list of string commands to pass to main.js
        workspace (str): workspace name
        timeout (int):  time to give command to complete (negative == infinite)

    Returns:
        (bool, str): returns tuple with (bool=result, str=value)
            caller must convert value to proper value

    """
    # Open local socket for IPC (result of command is posted to socket)
    result_server = ResultServer(debug=False)
    port = result_server.start()
    result = None

    # Remove timeout if negative number provided (inifinite timeout)
    if timeout < 0:
        timeout = None

    main_js = os.path.abspath(os.path.dirname(
        __file__) + "/../" + MAIN_JS_PATH)
    if not os.path.isfile(main_js):
        raise DSSError("Trouble finding main.js: %s" % main_js)

    cwd = os.path.abspath(os.path.dirname(__file__) + "/../")

    # Create list of args for calling dss exec
    cmd = [dss_path]
    if workspace:
        cmd.extend(["-data", workspace])
    cmd.extend(DSS_ARGS)

    # Create list of args for js script
    script_args = [main_js, cwd, str(port)]
    script_args.extend(commands)
    # Convert list to one string (necessary for rhino exec)
    script_args = map(str, script_args)
    script_args_str = " ".join(script_args)

    cmd.append(script_args_str)
    try:
        retcode = subprocess.call(cmd)
    except Exception as e:
        print(e)
        return (False, "Command Failed")

    # Wait on result to be populated
    result = result_server.get_result(timeout=timeout)

    return (retcode == 0, result)


def format_args(args):
    """Converts args dict to properly formatted cmd list for dss scripts
    """
    if type(args) is not dict:
        raise DSSError("Arguments passed must be of type 'dict'")

    arg_list = []
    for k in args:
        arg_list.append("--%s" % k)
        if type(args[k]) == dict:
            for k2 in args[k]:
                arg_list.append("-%s" % k2)
                arg_list.append(args[k][k2])
        else:
            pass

    return arg_list


def parse_response_float(response):
    """Handles the parsing of a string response representing a float

    All responses are sent as strings. In order to convert these strings to
    their python equivalent value, you must call a parse_response_* function.

    Args:
        response (str): response string to parse and convert to proper value

    Returns:
        (float): returns reponse string converted to float
    """

    parsed_response = float(response)

    return parsed_response


def parse_response_number(response):
    """Handles the parsing of a string response representing a number (no
    decimal)

    All responses are sent as strings. In order to convert these strings to
    their python equivalent value, you must call a parse_response_* function.

    Args:
        response (str): response string to parse and convert to proper value

    Returns:
        (int): returns reponse string converted to int or long
    """
    parsed_response = int(response)

    return parsed_response


def parse_response_list(response):
    """Handles the parsing of a string response representing a list

    All responses are sent as strings. In order to convert these strings to
    their python equivalent value, you must call a parse_response_* function.

    Args:
        response (str): response string to parse and convert to proper value

    Returns:
        (list): returns reponse string converted to list
    """
    element_sep = ";;"

    parsed_response = response.split(element_sep)

    return parsed_response


def parse_response_bool(response):
    """Handles the parsing of a string response representing a bool

    All responses are sent as strings. In order to convert these strings to
    their python equivalent value, you must call a parse_response_* function.

    Args:
        response (str): response string to parse and convert to proper value

    Returns:
        (bool): returns reponse string converted to bool
    """
    parsed_response = None
    if response.lower() == 'true':
        parsed_response = True
    elif response.lower() == 'false':
        parsed_response = False
    else:
        raise DSSError("Invalid boolean response")

    return parsed_response
