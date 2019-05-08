import os
from dsclient import DebugServer, DebugSession
from tiflash.core.helpers import (
    resolve_ccs_path,
    DEPRECATED,
    resolve_ccxml_path,
    resolve_serno,
    resolve_devicetype,
    resolve_connection,
    resolve_session_args,
    compare_session_args,
)
from tiflash.utils.dss import launch_server, resolve_ccs_exe
from tiflash.utils.ccs import find_ccs, get_workspace_dir, __get_ccs_exe_path
from tiflash.utils.ccxml import get_ccxml_directory, add_serno


class TIFlashError(Exception):
    """Generic TI Flash error"""

    pass


class TIFlashSession(object):
    """TIFlash Session object for interacting with device over DSS"""

    def __init__(
        self,
        ccs=None,
        ccs_path=None,
        ccs_version=None,
        serno=None,
        devicetype=None,
        connection=None,
        ccxml=None,
        fresh=False,
        keep_alive=False,
    ):
        """Instantiates TIFlashSession object.

        Args:
            ccs (str, optional): DEPRECATED: ccs version or path to ccs (default is latest installation found)
            ccs_path (str, optional): path to ccs installation or directory of installation
            ccs_version (str, optional): version number of ccs to use (default=latest)
            serno (str, optional): serial number of device
            serialnum (str, optional): serial number of device
            devicetype (str, optional): name of devicetype
            connection (str, optional): name of connection
            ccxml (str, optional): full path to ccxml file to use
            fresh (bool, optional): create a fresh ccxml file instead of using existing (default=False)
            debug (bool, optional): output extra debugging information (default=False)
            keep_alive (bool, optional): keep the debugserver running even after TIFlashSession object is destroyed (default=False)

        Warning:
            Deprecated parameters are listed below. These parameters will be removed in future version of TIFlash:
            - ccs: use `ccs_version` and `ccs_path` to specifiy which ccs
              installation to use

        """
        self.keep_alive = keep_alive
        self.workspace = get_workspace_dir()  # TODO: append uuid
        self.ccxml_path = None

        # Set CCS path
        self.ccs_path = None
        self.__configure_ccs(ccs=ccs, ccs_version=ccs_version, ccs_path=ccs_path)

        ccs_exe = resolve_ccs_exe(self.ccs_path)

        # Launch DebugServer
        self._server_pid, self._server_port = launch_server(ccs_exe, self.workspace)

        # Connect DSClient
        self._dsclient = DebugServer(port=self._server_port)

        # Set Session args
        if any([serno, devicetype, connection, ccxml]):
            self.__configure_session(
                serno=serno,
                devicetype=devicetype,
                connection=connection,
                ccxml=ccxml,
                fresh=fresh,
            )

    def __configure_ccs(self, ccs=None, ccs_version=None, ccs_path=None):
        """Finds and sets the path to CCS installation to use

        Args:
            ccs (str, optional): DEPRECATED: ccs version or path to ccs (default is latest installation found)
            ccs_path (str, optional): path to ccs installation or directory of installation
            ccs_version (str, optional): version number of ccs to use (default=latest)

        Warning:
            Can only be run once (before launch of DebugServer).
        """
        if self.ccs_path is not None:
            raise Exception("CCS path already set to: %s" % self.ccs_path)

        # Resolve which ccs installation to use
        if ccs is not None:
            DEPRECATED(
                "'ccs' arg is deprecated and will be removed in a later version of tiflash; use 'ccs_path' and 'ccs_version' parameters instead.",
                stacklevel=4,
            )
            self.ccs_path = resolve_ccs_path(ccs)
        else:
            self.ccs_path = find_ccs(version=ccs_version, ccs_prefix=ccs_path)

    def __configure_session(
        self, serno=None, devicetype=None, connection=None, ccxml=None, fresh=False
    ):
        """
        Args:
            serno (str, optional): serial number of device
            serialnum (str, optional): serial number of device
            devicetype (str, optional): name of devicetype
            connection (str, optional): name of connection
            ccxml (str, optional): full path to ccxml file to use
            fresh (bool, optional): create a fresh ccxml file instead of using existing (default=False)
        """

        session_args = resolve_session_args(
            self.ccs_path,
            ccxml=ccxml,
            serno=serno,
            devicetype=devicetype,
            connection=connection,
        )
        self.ccxml_path = session_args["ccxml"]
        self.serno = session_args["serno"]
        self.devicetype = session_args["devicetype"]
        self.connection = session_args["connection"]

        # Compare resolved session args with what's already in ccxml
        if self.ccxml_path is not None:
            # Determine if ccxml needs to be regenerated
            fresh = fresh or not compare_session_args(
                self.ccxml_path,
                serno=self.serno,
                devicetype=self.devicetype,
                connection=self.connection,
            )
        else:
            fresh = True

        # Create ccxml if needed
        if fresh:
            if self.ccxml_path is not None:
                directory, name = os.path.split(self.ccxml_path)
            else:
                name = directory = None

            self.ccxml_path = self.create_config(
                name=name,
                directory=directory,
                serno=self.serno,
                devicetype=self.devicetype,
                connection=self.connection,
            )

        # Set ccxml file
        try:
            self._dsclient.set_config(self.ccxml_path)
        except Exception as e:
            raise TIFlashError(e)

    def create_config(self, name=None, directory=None, **config):
        """Generates a ccxml file using the provided parameters

        Args:
            name (str, optional): name to give ccxml file (default is: <serno>.ccxml, <devicetype>.ccxml or <connection.ccxml>)
            directory (str, optional): directory to place ccxml file (default = default CCSTargetConfigurations directory)
            **config (**kwargs): key-word args specifying possible configuration parameters to use when creating ccxml

        Returns:
            str: full path to generated ccxml file

        Raises:
            Exception: raised if error generating ccxml file
        """
        serno = config.get("serno", None)
        devicetype = config.get("devicetype", None)
        connection = config.get("connection", None)

        # Determine ccxml file name to use
        if name is None:
            name = serno or devicetype or connection or "UNTITLED"

        if not name.endswith(".ccxml"):
            name += ".ccxml"

        if directory is None:
            directory = get_ccxml_directory()

        ccxml_path = os.path.join(directory, name)

        self._dsclient.create_config(
            name, connection=connection, device=devicetype, directory=directory
        )

        if not os.path.exists(ccxml_path):
            raise TIFlashError(
                "Could not find ccxml file after generating: %s" % ccxml_path
            )

        if serno is not None:
            add_serno(ccxml_path, serno, self.ccs_path)

        return ccxml_path

    def attach_ccs(self, keep_alive=False):
        """Opens a CCS GUI for the device in use
        Args:
            keep_alive (bool): keep the DebugServer process running in
                background after object is destroyed
        """
        try:
            self.keep_alive = keep_alive
            self._dsclient.attach_ccs()
        except Exception as e:
            raise TIFlashError(e)

    def get_config(self):
        """Returns the full path to the ccxml file in use for TIFlashSession

        Returns:
            str: full path to .ccxml file in use for TIFlashSession
                (returns None if ccxml has not be set yet)
        """
        return self.ccxml_path

    def get_list_of_connections(self):
        """Returns a list of available connections

        Returns:
            list: list of available connection names
        """
        try:
            return self._dsclient.get_list_of_connections()
        except Exception as e:
            raise TIFlashError(e)

    def get_list_of_cpus(self):
        """Returns a list of available cpu/core names for the device in use

        Returns:
            list: list of available core/cpu names for the device in use

        Raises:
            Exception: raised if no config set yet
        """
        try:
            return self._dsclient.get_list_of_cpus()
        except Exception as e:
            raise TIFlashError(e)

    def get_list_of_devices(self):
        """Returns a list of available devices

        Returns:
            list: list of available device names
        """
        try:
            return self._dsclient.get_list_of_devices()
        except Exception as e:
            raise TIFlashError(e)

    def get_core(self, name):
        """Returns Core object representing a device core

        Args:
            name (str): name of core to retrieve (can be regex pattern)

        Returns:
            dsclient.DebugSession: DebugSession object representing the device core
        """
        session = None
        try:
            session = self._dsclient.get_session(name)
        except:
            session = self._dsclient.open_session(name)

        return Core(session)

    def __del__(self):
        if self.keep_alive is False:
            # Close down server
            self._dsclient.kill()

            # Ensure process is closed down properly
            try:
                # timeout param only availble in python3
                self._server_pid.wait(timeout=3)
            except Exception:  # TimeoutExpired
                self._server_pid.terminate()


class Core(object):
    """Class representing device core"""

    def __init__(self, debugsession):
        """Instantiates Core object representing a device core

        Args:
            debugsession (dsclient.DebugSession): debugsession instance
                returned from DebugServer.open_session()

        Warning:
            This class should not be directly instantiated. Instead use the
            TIFlashSession.get_core() function
        """
        try:
            self._debugsession = debugsession
        except Exception as e:
            raise TIFlashError(e)

    def connect(self):
        """Connect to core"""
        try:
            self._debugsession.connect()
        except Exception as e:
            raise TIFlashError(e)

    def disconnect(self):
        """Disconnects from core"""
        try:
            self._debugsession.disconnect()
        except Exception as e:
            raise TIFlashError(e)

    def erase(self):
        """Erases device's flash memory.  """
        try:
            self._debugsession.erase()
        except Exception as e:
            raise TIFlashError(e)

    def reset(self):
        """Resets device."""
        try:
            self._debugsession.reset()
        except Exception as e:
            raise TIFlashError(e)

    def load(self, file, binary=False, address=None):
        """Loads image into device's flash.

        Args:
            file (str): full path to file to load into flash
            binary (boolean, optional): specify to load image as binary (default = False)
            address (int, optional): specify to load binary image at specifc address (only to be used when 'binary' is True; default=0x0)


        Raises:
            Exception if image fails to load
        """
        try:
            self._debugsession.load(file, binary=binary, address=address)
        except Exception as e:
            raise TIFlashError(e)

    def verify(self, file, binary=False, address=None):
        """Verifies image in device's flash.

        Args:
            file (str): full path to file to verify in flash
            binary (boolean, optional): specify to verify image as binary (default = False)
            address (int, optional): specify to verify binary image at specifc address (only to be used when 'binary' is True; default=0x0)


        Raises:
            Exception if image fails verification process
        """
        try:
            self._debugsession.verify(file, binary=binary, address=address)
        except Exception as e:
            raise TIFlashError(e)

    def evaluate(self, expression, file=None):
        """Evaluates an expression (after loading optional symbols file)

        Args:
            expression (str): C/GEL expression to evaluate
            file (str, optional): path to file containing symbols to load before evaluating

        Returns:
            int: result of evaluated expression


        Raises:
            Exception if expression is invalid.
        """
        try:
            return self._debugsession.evaluate(expression, file=file)
        except Exception as e:
            raise TIFlashError(e)

    def read_data(self, address, page=0, num_bytes=1):
        """Read memory from device

        Args:
            address (int): address to read data from
            page (int, optional): page in memory to get address from (default = 0)
            num_bytes (int, optional): number of bytes to read

        Returns:
            list: list of bytes(ints) read


        Raises:
            Exception if address location is invalid.
        """
        try:
            return self._debugsession.read_data(address, page=page, num_bytes=num_bytes)
        except Exception as e:
            raise TIFlashError(e)

    def write_data(self, data, address, page=0):
        """Write to memory on device

        Args:
            data (list): list of bytes (ints) to write to memory
            address (int): address to read data from
            page (int, optional): page in memory to get address from (default = 0)


        Raises:
            Exception if address location is invalid.
        """
        try:
            return self._debugsession.write_data(data, address, page=page)
        except Exception as e:
            raise TIFlashError(e)

    def read_register(self, name):
        """Read value from register

        Args:
            name (str): register name to read

        Returns:
            int: value of register read


        Raises:
            Exception if register name is invalid.
        """
        try:
            return self._debugsession.read_register(name)
        except Exception as e:
            raise TIFlashError(e)

    def write_register(self, name, value):
        """Write value to register on device

        Args:
            name (str): register name to write to
            value (int): value to write to register


        Raises:
            Exception if register name is invalid.
        """
        try:
            self._debugsession.write_register(name, value)
        except Exception as e:
            raise TIFlashError(e)

    def get_option(self, option_id):
        """Get the value of a device option

        Args:
            option_id (str): name of device option

        Returns:
            any: value of option


        Raises:
            Exception if option id is invalid.
        """
        try:
            return self._debugsession.get_option(option_id)
        except Exception as e:
            raise TIFlashError(e)

    def set_option(self, option_id, value):
        """Set the value of a device option

        Args:
            option_id (str): name of device option
            value (any): value to set option to


        Raises:
            Exception if option id is invalid.
        """
        try:
            self._debugsession.set_option(option_id, value)
        except Exception as e:
            raise TIFlashError(e)

    def perform_operation(self, opcode):
        """Performs flash operation

        Args:
            opcode (str): name of operation to perform (opcode)

        Returns:
            any: returns value of performing operation


        Raises:
            Exception if opcode is invalid.
        """
        try:
            return self._debugsession.perform_operation(opcode)
        except Exception as e:
            raise TIFlashError(e)

    def run(self, asynchronous=False):
        """Issues the run command to the device

        Args:
            asynchronous (boolean, optional): run and return control immediately (default = False)
        """
        try:
            self._debugsession.run(asynchronous=asynchronous)
        except Exception as e:
            raise TIFlashError(e)

    def halt(self, wait=False):
        """Halts the device

        Args:
            wait (boolean): wait until device is actually halted before returning
        """
        try:
            self._debugsession.halt(wait=wait)
        except Exception as e:
            raise TIFlashError(e)
