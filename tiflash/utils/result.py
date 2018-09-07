"""
Module for creating a socket for js/main.js script to post
command results to (used for IPC)


Author: Cameron Webb
Date: March 2018
Contact: webbjcam@gmail.com

"""

import socket
import threading
from sys import version_info as pyversion

HOST = "localhost"
PORT = 19876    # Port to open socket on
MAX_PORTS = 3   # Determines number of tiflash processes can run simultaneously
MAX_CLIENTS = 1
if pyversion[0] == 2:
    SOCK_TIMEOUT = None   # timeouts don't seem to work for py2
else:
    SOCK_TIMEOUT = 60   # timeout to wait for result


class ResultServerError(Exception):
    """Generic Error for Result Server"""
    pass


class ResultServer(object):
    """ Class for receiving a result over a local socket
        from js/main.js subprocess.

    Creates local socket for the js/main.js subprocess to post the result of
    a command to.

    Args:
        port (int): port to create socket on

    """

    def __init__(self, host=HOST, port=PORT, debug=False):
        """ Initializes and starts the ResultServer

        Args:
            host (str): host to open socket; should ALWAYS be 'localhost'
            port (int): port to open socket on;
            debug (bool): choose to include debug messages

        """
        self.host = host
        self.port = port
        self.debug = debug

        self.result = None
        self.server_thread = None
        # Server Running Event (set only when server is running)
        self.running = threading.Event()

    def __del__(self):
        # Notify server to stop running
        self.running.clear()

    def start(self):
        """Starts the Result Server"""
        self.server_thread = threading.Thread(
            target=self._start_server, args=(self.debug,))
        self.server_thread.start()

        # Wait for server running event
        if not self.running.wait(timeout=0.5):  # timeout=0 feels to risky
            raise ResultServerError("Result Server failed to start")

        return self.port

    def get_result(self, timeout=None):
        """ Gets the result posted to the socket. Blocks until result is posted
            to socket, unless a timeout is given.

        Args:
            timeout (int): time to wait for result to be posted to socket.
                If 'None' will block/wait forever. If '0' will not block.

        """
        if self.server_thread.isAlive() is True:
            self.server_thread.join(timeout=timeout)

            # Thread should only be alive if timeout was exceeded
            if self.server_thread.isAlive is True:
                return None

        if type(self.result) == str:
            return self.result.strip()
        else:
            return self.result

    def _start_server(self, debug):
        """ Creates the socket for the result to be posted to.

        """
        result = ""
        if debug:
            print("Starting server...")
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:   #Py3
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.settimeout(SOCK_TIMEOUT)

        # Try up to MAX_PORTS different ports
        for i in range(MAX_PORTS):
            try:
                s.bind((self.host, self.port + i))
                self.port = self.port + i
                break
            except Exception:
                continue
        else:
            raise ResultServerError("""Too many result sockets in use. (At
                least %d)""" % MAX_PORTS)

        # Set/Fire server running event
        self.running.set()

        s.listen(MAX_CLIENTS)
        conn, addr = s.accept()
        # with conn: #Py3
        if debug:
            print("Connected by", addr)

        # Run until server running event is cleared
        while self.running.is_set():
            try:
                data = conn.recv(1024)
            except socket.timeout:
                result = None
                break
            if not data:
                break
            result += data.decode("utf-8").strip()

        if debug:
            print("Received: %s from %s" % (result, addr))

        self.result = result

        s.close()
