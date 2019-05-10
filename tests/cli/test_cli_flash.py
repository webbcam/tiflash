import pytest
import subprocess

from clihelpers import get_cmd_with_device_params


class TestFlashCli:
    def test_basic_flash(self, tdev):
        """Tests simple flash on each device in devices.cfg"""

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["flash", '"%s"' % tdev["hex-image"]])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_binary_flash(self, tdev):
        """Creates a binary image from the hex image and tries to flash the
        device.

        Checks two test cases:
        1) fails when trying to flash binary image with
            'bin' bool set to False;
        2) passes when trying to flash binary image with
            'bin' bool set to True;
        """
        # Basic Binary Test
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["flash", '"%s"' % tdev["binary-image"], "--bin"])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

        # Flashing binary without specifying binary=True
        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(tdev)

            cmd.extend(["flash", '"%s"' % tdev["binary-image"]])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)

        # Flashing hex image with specifying binary image = True
        with pytest.raises(subprocess.CalledProcessError):
            cmd = get_cmd_with_device_params(tdev)

            cmd.extend(["flash", '"%s"' % tdev["hex-image"], "--bin"])
            cmd_str = " ".join(cmd)

            subprocess.check_call(cmd_str, shell=True)
