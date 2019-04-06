import os
import pytest

from tiflash.utils import dss


class TestDSS():
    def test_launch_server(t_env):
        """Tests DebugServer process can be launched successfully."""
        p, port = dss.launch_server(tenv["ccs-exe"], tenv["workspace"])
        assert p.poll() is None

        p.terminate()
