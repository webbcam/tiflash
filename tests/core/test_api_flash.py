import pytest
import tiflash

class TestFlashApi():

    def test_basic_flash(self, tdev):
        """Tests simple flash on each device in devices.cfg"""
        assert tdev['hex-image'] is not None
        result = tiflash.flash(tdev['hex-image'], serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result is True

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
        assert tdev['binary-image'] is not None
        result = tiflash.flash(tdev['binary-image'], binary=True, serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])
        assert result is True

        # Flashing binary without specifying binary=True
        assert tdev['binary-image'] is not None
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.flash(tdev['binary-image'], binary=False, serno=tdev['serno'],
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])

        # Flashing hex image with specifying binary image = True
        assert tdev['hex-image'] is not None
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.flash(tdev['hex-image'], binary=True, serno=tdev['serno'],
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])
