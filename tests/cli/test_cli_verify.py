import pytest
import intelhex
import subprocess

from clihelpers import get_cmd_with_device_params

@pytest.mark.usefixtures("device")
class TestVerifyCli():

    def test_basic_verify(self, device):
        """Tests simple flash on each device in devices.cfg"""
        cmd = get_cmd_with_device_params(device)

        # First Flash image
        cmd.extend(["flash", "\"%s\"" % device["image"]])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

        # Then Verify image
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["verify", "\"%s\"" % device["image"]])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


    @pytest.mark.xfail
    def test_binary_verify(self, device):
        """Creates a binary image from the hex image and tries to flash the
        device.

        Checks two test cases:
        1) fails when trying to flash binary image with
            'bin' bool set to False;
        2) passes when trying to flash binary image with
            'bin' bool set to True;
        """
        # Ensure image is a hex file
        assert device['image'].endswith(".hex")
        hex_path = device['image']
        bin_path = hex_path[:-3] + "bin"

        # Convert .hex image to .bin
        intelhex.hex2bin(hex_path, bin_path)

        # Basic Binary Flash
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["flash", "\"%s\"" % bin_path, "--bin"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

        # Basic Binary Verify
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["verify", "\"%s\"" % bin_path, "--bin"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


        # Verifying binary without specifying binary=True
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["verify", "\"%s\"" % bin_path])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)


        # Verify hex image with specifying binary image = True
        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(device)

            cmd.extend(["verify", "\"%s\"" % hex_path, "--bin"])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)
