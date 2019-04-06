import os
import re
import json
import socket
import subprocess


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
        os.path.join(os.path.dirname(os.path.dirname(__file__)),"components", "debugserver-js")
    )
    ccsexe = [
        ccs_exe,
        "-noSplash",
        "-application",
        "com.ti.ccstudio.apps.runScript",
        "-ccs.script",
    ]
    ccsexe.append(server_script)
    ccsexe.append("-ccs.rhinoArgs")

    p = subprocess.Popen(ccsexe, stdout=subprocess.PIPE)

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
