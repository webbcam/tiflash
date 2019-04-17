from dsclient import DebugServer, DebugSession
from tiflash.core.helpers import (
    resolve_ccs_path,
    DEPRECATED,
    resolve_ccxml_path,
    resolve_serno,
    resolve_devicetype,
    resolve_connection,
    compare_session_args,
)
from tiflash.utils.dss import launch_server, resolve_ccs_exe
from tiflash.utils.ccs import find_ccs, get_workspace_dir, __get_ccs_exe_path


class TIFlashSession(object):
    """TIFlash Session object for interacting with device over DSS"""

    def __init__(self, ccs=None, ccs_path=None, ccs_version=None, keep_alive=False):
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
        self.workspace = get_workspace_dir()

        # Set CCS path
        self.ccs_path = None
        self.__configure_ccs(ccs=ccs, ccs_version=ccs_version, ccs_path=ccs_path)

        ccs_exe = resolve_ccs_exe(self.ccs_path)

        # Launch DebugServer
        self._server_pid, self._server_port = launch_server(ccs_exe, self.workspace)

        # Connect DSClient
        self._dsclient = DebugServer(port=self._server_port)

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
        self.ccxml_path = resolve_ccxml_path(
            ccxml=ccxml, serno=serno, devicetype=devicetype
        )

        self.serno = resolve_serno(serno=serno, ccxml=self.ccxml_path)

        self.devicetype = resolve_devicetype(
            devicetype=devicetype,
            serno=self.serno,
            ccxml=self.ccxml_path,
            ccs_path=self.ccs_path,
        )

        self.connection = resolve_connection(
            connection=self.connection,
            ccxml=self.ccxml_path,
            devicetype=self.devicetype,
            ccs_path=self.ccs_path,
        )

        # Compare resolved session args with what's already in ccxml
        if self.ccxml_path is not None:
            # Determine if ccxml needs to be regenerated
            fresh = fresh or compare_session_args(self.ccxml_path,
                    serno=self.serno, devicetype=self.devicetype,
                    connection=self.connection)

        # Create ccxml if needed


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
