import pytest
import subprocess

from clihelpers import get_cmd_with_device_params


class TestXDS110Cli:
    def test_basic_xds110_reset(self, tdev):
        """Tests simple xds110_reset on each device in devices.cfg"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["xds110-reset"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_basic_xds110_reset_fail(self, tdev):
        """Tests xds110_reset fails when garbage serno used"""
        old_serno = tdev["serno"]
        tdev["serno"] = "GARBAGE"
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["xds110-reset"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)
        tdev["serno"] = old_serno

    def test_basic_xds110_list(self, tdev, tenv):
        """Tests xds110_list returns list of all connected devices"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["xds110-list"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    @pytest.mark.skip(
        reason="Issue with board connections after xds110 upgrade in testing; Please run manually"
    )
    def test_basic_xds110_upgrade(self, tdev):
        """Tests simple xds110_upgrade on each device in devices.cfg"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["xds110-upgrade"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_basic_xds110_upgrade_fail(self, tdev):
        """Tests xds110_upgrade fails when garbage serno used"""
        old_serno = tdev["serno"]
        tdev["serno"] = "GARBAGE"
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["xds110-upgrade"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)
        tdev["serno"] = old_serno
