import pytest

import tiflash

@pytest.mark.usefixtures("device")
class TestXDS110Api():

    def test_basic_xds110reset(self, device):
        """Tests simple xds100reset on each device in devices.cfg"""
        result = tiflash.xds110reset(serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True

    def test_basic_xds110reset_fail(self, device):
        """Tests xds100reset fails when garbage serno used"""
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.xds110reset(serno="GARBAGE",
                                connection=device['connection'],
                                devicetype=device['devicetype'])
