import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

class TestResetCli():

    def test_basic_reset(self, tdev):
        """Tests simple reset on each device in devices.cfg"""

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["reset"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)
