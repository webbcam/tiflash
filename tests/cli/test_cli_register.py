import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

class TestRegisterCli():

    def test_basic_register_read(self, tdev):
        """Tests simple register read"""
        REGNAME = "PC"

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["register-read", "\"%s\"" % REGNAME])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_basic_register_write(self, tdev):
        """Tests simple register write"""
        REGNAME = "R1"
        VALUE = "0xBEEF"

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["register-write", "\"%s\"" % REGNAME, VALUE])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    def test_invalid_register_read(self, tdev):
        """Tests an Error is raised when trying to access invalid register for
        register read"""
        INVALID_REGNAME = "INVALIDREGNAME"

        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(tdev)

            cmd.extend(["register-read", "\"%s\"" % INVALID_REGNAME])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)



    @pytest.mark.xfail
    def test_invalid_register_write(self, tdev):
        """Tests an Error is raised when trying to access invalid register for
        register write"""
        INVALID_REGNAME = "PC"
        VALUE = "0xFFFFFF"

        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(tdev)

            cmd.extend(["register-write", "\"%s\"" % INVALID_REGNAME, VALUE])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)
