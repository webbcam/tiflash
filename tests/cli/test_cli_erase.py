import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

@pytest.mark.usefixtures("device")
class TestEraseCli():

    def test_basic_erase(self, device):
        """Tests simple erase on each device in devices.cfg"""

        cmd = get_cmd_with_device_params(device)

        cmd.append("erase")
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)
