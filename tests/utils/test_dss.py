import os
import pytest
import time

from tiflash.utils import dss

class TestDSS():
    def test_launch_server(self, tenv):
        """Tests DebugServer process can be launched successfully."""
        ccs_exe = dss.resolve_ccs_exe(tenv["paths"]["ccs"])
        p, port = dss.launch_server(ccs_exe, tenv["paths"]["workspace"])
        assert p.poll() is None

        time.sleep(3)

        p.terminate()
