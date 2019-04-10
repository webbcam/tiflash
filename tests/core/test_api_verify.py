import pytest
import intelhex

import tiflash


class TestVerifyApi():

    def test_basic_verify(self, tdev):
        """Tests simple flash on each device in devices.cfg"""
        if tdev['hex-image'] not in tdev.keys():
            pytest.skip("No image provided in setup.cfg for this device")

        result = tiflash.flash(tdev['hex-image'], serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])
        if result is False:
            pytest.skip("Flashing of image needs to work in order for this"
                "test to run")

        result = tiflash.verify(tdev['hex-image'], serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result is True


    @pytest.mark.xfail
    def test_binary_verify(self, tdev):
        """Creates a binary image from the hex image and tries to flash the
        device.

        Checks two test cases:
        1) fails when trying to verify binary image with
            'bin' bool set to False;
        2) passes when trying to verify binary image with
            'bin' bool set to True;
        """

        # Basic Binary Test
        result = tiflash.flash(tdev['binary-image'], binary=True, serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        if result is False:
            pytest.skip("Flashing of image needs to work in order for this"
                "test to run")

        result = tiflash.verify(tdev['binary-image'], binary=True, serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result is True

        # Verifying binary without specifying binary=True
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.verify(tdev['binary-image'], binary=True, serno=tdev['serno'],
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])

        # Verifying hex image with specifying binary image = True
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.verify(tdev['hex-image'], binary=True, serno=tdev['serno'],
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])
