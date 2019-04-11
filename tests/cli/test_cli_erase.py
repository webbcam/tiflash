import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

class TestEraseCli():

    def test_basic_erase(self, tdev):
        """Tests simple erase on each device in devices.cfg"""

        cmd = get_cmd_with_device_params(tdev)

        cmd.append("erase")
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)
