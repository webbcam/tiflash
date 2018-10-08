import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

@pytest.mark.usefixtures("device")
class TestXDS110Cli():

    def test_basic_xds110_reset(self, device):
        """Tests simple xds110_reset on each device in devices.cfg"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["xds110-reset"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_basic_xds110_reset_fail(self, device):
        """Tests xds110_reset fails when garbage serno used"""
        old_serno = device['serno']
        device['serno'] = "GARBAGE"
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["xds110-reset"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)
        device['serno'] = old_serno

    def test_basic_xds110_list(self, device, t_env):
        """Tests xds110_list returns list of all connected devices"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["xds110-list"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_basic_xds110_upgrade(self, device):
        """Tests simple xds110_upgrade on each device in devices.cfg"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["xds110-upgrade"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_basic_xds110_upgrade_fail(self, device):
        """Tests xds110_upgrade fails when garbage serno used"""
        old_serno = device['serno']
        device['serno'] = "GARBAGE"
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["xds110-upgrade"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)
        device['serno'] = old_serno
