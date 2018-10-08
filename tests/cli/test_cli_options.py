import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

@pytest.mark.usefixtures("device")
class TestOptionsCli():

    # Getters
    def test_basic_get_option(self, device):
        """Tests basic get_option function"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-get", "\"%s\"" % "ResetOnRestart"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_get_option_with_preop(self, device):
        """Tests get_option with a preop"""
        if 'ieee' not in device.keys():
            pytest.skip("No IEEE Address provided in setup.cfg for this device")

        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-get", "\"%s\"" % "DeviceIeeePrimary", "-op", "\"ReadPriIeee\""])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_get_invalid_option(self, device):
        """Tests get_option throws error when invalid option id provided"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-get", "\"%s\"" % "InvalidOption"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)

    def test_get_option_invalid_preop(self, device):
        """Tests get_option raises error when invalid preop provided"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-get", "\"%s\"" % "DeviceInfoRevision", "-op", "InvalidPreOp"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)


    # Setters
    @pytest.mark.xfail
    def test_basic_set_option(self, device):
        """Tests basic set_option function"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-set", "\"%s\"" % "ResetOnRestart", "\"%s\"" % value])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    # List
    def test_list_options(self, device):
        """Tests all options returned in list are valid"""
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-list"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_list_single_option(self, device):
        """Tests listing of one specified option"""
        option_to_test = "DeviceInfoRevision"

        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-list", "\"%s\"" % option_to_test])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    @pytest.mark.xfail
    def test_list_single_nonexistant_option(self, device):
        """Tests listing of specified option that does not exist"""
        option_to_test = "InvalidOption"

        cmd = get_cmd_with_device_params(device)

        cmd.extend(["options-list", "\"%s\"" % option_to_test])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)
