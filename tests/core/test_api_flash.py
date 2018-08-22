import pytest
import intelhex

import tiflash

@pytest.mark.usefixtures("device")
class TestFlashApi():

    def test_basic_flash(self, device):
        """Tests simple flash on each device in devices.cfg"""
        assert device['image'] is not None
        result = tiflash.flash(device['image'], serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True

    def test_binary_flash(self, device):
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

        # Basic Binary Test
        result = tiflash.flash(bin_path, binary=True, serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])
        assert result is True

        # Flashing binary without specifying binary=True
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.flash(bin_path, binary=False, serno=device['serno'],
                                connection=device['connection'],
                                devicetype=device['devicetype'])

        # Flashing hex image with specifying binary image = True
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.flash(hex_path, binary=True, serno=device['serno'],
                                connection=device['connection'],
                                devicetype=device['devicetype'])
