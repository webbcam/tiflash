import os
import re
import json
import socket
import subprocess
import platform


def resolve_ccs_exe(ccs_path):
    """Returns the ccstudio executable given the ccs installation path

    Args:
        ccs_path (str): full path to ccs installation

    Returns:
        str: full path to the ccs executable
    """
    exe = None
    system = platform.system()
    if system == "Windows":
        exe = "eclipse/eclipsec.exe"
    elif system == "Linux":
        exe = "eclipse/ccstudio"
    elif system == "Darwin":
        exe = "eclipse/Ccstudio.app/Contents/MacOS/ccstudio"
    else:
        raise Exception("Unsupported Operating System: %s" % system)

    ccs_exe = os.path.join(ccs_path, exe)
    ccs_exe = os.path.normpath(ccs_exe)

    if not os.path.exists(ccs_exe):
        raise Exception("Could not find ccstudio executable: %s" % ccs_exe)

    return ccs_exe


def launch_server(ccs_exe, workspace):
    """Launches DebugServer process

    Args:
        ccs_exe (str): full path to ccs executable
        workspace (str): full path to workspace to use

    Returns:
        (subprocess.PID, int): returns tuple containing process id and port number
    """
    server_script = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "server.js")
    )
    os.environ["DSS_SCRIPTING_ROOT"] = os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "components", "debugserver-js"
        )
    )
    ccsexe = [
        ccs_exe,
        "-noSplash",
        "-application",
        "com.ti.ccstudio.apps.runScript",
        "-data",
        workspace,
        "-ccs.script",
    ]
    ccsexe.append(server_script)
    ccsexe.append("-ccs.rhinoArgs")

    p = subprocess.Popen(ccsexe, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if p.poll() is not None:
        raise Exception("Could not start server process")

    # Wait until Debug Server has started
    line = ""
    while "PORT" not in str(line):
        line = p.stdout.readline()
    try:
        m = re.search("PORT: ([0-9]+)", str(line))
        port = int(m.group(1))
    except:
        p.terminate()
        raise Exception("Could not retrieve port from debugserver process.")

    return (p, port)
