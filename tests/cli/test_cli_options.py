import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

class TestOptionsCli():

    # Getters
    def test_basic_get_option(self, tdev):
        """Tests basic get_option function"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-get", "\"%s\"" % tdev['option']])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    @pytest.mark.skip
    def test_get_option_with_preop(self, tdev):
        """Tests get_option with a preop"""
        if 'preop' not in tdev.keys():
            pytest.skip("No preop provided for device")

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-get", "\"%s\"" % tdev['preop-option'], "-op", "\"%s\"" % tdev['preop']])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_get_invalid_option(self, tdev):
        """Tests get_option throws error when invalid option id provided"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-get", "\"%s\"" % "InvalidOption"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)

    def test_get_option_invalid_preop(self, tdev):
        """Tests get_option raises error when invalid preop provided"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-get", "\"%s\"" % tdev['preop-option'], "-op", "InvalidPreOp"])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)


    # Setters
    def test_basic_set_option(self, tdev):
        """Tests basic set_option function"""
        cmd = get_cmd_with_device_params(tdev)
        value = tdev['option-val']

        cmd.extend(["options-set", "\"%s\"" % tdev['option'], "\"%s\"" % value])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    # List
    def test_list_options(self, tdev):
        """Tests all options returned in list are valid"""
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-list"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_list_single_option(self, tdev):
        """Tests listing of one specified option"""
        option_to_test = tdev['option']

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-list", "\"%s\"" % option_to_test])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_list_single_nonexistant_option(self, tdev):
        """Tests listing of specified option that does not exist"""
        option_to_test = "InvalidOption"

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["options-list", "\"%s\"" % option_to_test])
        cmd_str = " ".join(cmd)

        #with pytest.raises(subprocess.CalledProcessError):
        subprocess.check_call(cmd_str, shell=True)
