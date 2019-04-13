import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

class TestVerifyCli():

    def test_basic_verify(self, tdev):
        """Tests simple flash on each device in devices.cfg"""
        cmd = get_cmd_with_device_params(tdev)

        # First Flash image
        cmd.extend(["flash", "\"%s\"" % tdev["hex-image"]])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

        # Then Verify image
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["verify", "\"%s\"" % tdev["hex-image"]])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    @pytest.mark.xfail
    def test_binary_verify(self, tdev):
        """Creates a binary image from the hex image and tries to flash the
        device.

        Checks two test cases:
        1) fails when trying to flash binary image with
            'bin' bool set to False;
        2) passes when trying to flash binary image with
            'bin' bool set to True;
        """
        # Basic Binary Flash
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["flash", "\"%s\"" % tdev['binary-image'], "--bin"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

        # Basic Binary Verify
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["verify", "\"%s\"" % tdev['binary-image'], "--bin"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


        # Verifying binary without specifying binary=True
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["verify", "\"%s\"" % tdev['binary-image']])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


        # Verify hex image with specifying binary image = True
        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(tdev)

            cmd.extend(["verify", "\"%s\"" % tdev['hex-image'], "--bin"])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)
