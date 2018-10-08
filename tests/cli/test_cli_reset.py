import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

@pytest.mark.usefixtures("device")
class TestResetCli():

    def test_basic_reset(self, device):
        """Tests simple reset on each device in devices.cfg"""

        cmd = get_cmd_with_device_params(device)

        cmd.extend(["reset"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)
