import pytest
import intelhex


from tiflash import core, TIFlashError


@pytest.mark.usefixtures("device")
class TestVerifyApi():

    def test_basic_verify(self, device):
        """Tests simple flash on each device in devices.cfg"""
        if device['image'] is None:
            pytest.skip("No image provided in setup.cfg for this device")

        result = core.flash(device['image'], serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])
        if result is False:
            pytest.skip("Flashing of image needs to work in order for this"
                "test to run")

        result = core.verify(device['image'], serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True


    def test_binary_verify(self, device):
        """Creates a binary image from the hex image and tries to flash the
        device.

        Checks two test cases:
        1) fails when trying to verify binary image with
            'bin' bool set to False;
        2) passes when trying to verify binary image with
            'bin' bool set to True;
        """
        # Ensure image is a hex file
        assert device['image'].endswith(".hex")
        hex_path = device['image']
        bin_path = hex_path[:-3] + "bin"

        # Convert .hex image to .bin
        intelhex.hex2bin(hex_path, bin_path)

        # Basic Binary Test
        result = core.flash(bin_path, binary=True, serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        if result is False:
            pytest.skip("Flashing of image needs to work in order for this"
                "test to run")

        result = core.verify(bin_path, binary=True, serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])
        assert result is True

        # Verifying binary without specifying binary=True
        with pytest.raises(TIFlashError):
            result = core.verify(bin_path, binary=True, serno=device['serno'],
                                connection=device['connection'],
                                devicetype=device['devicetype'])

        # Verifying hex image with specifying binary image = True
        with pytest.raises(TIFlashError):
            result = core.verify(hex_path, binary=True, serno=device['serno'],
                                connection=device['connection'],
                                devicetype=device['devicetype'])
