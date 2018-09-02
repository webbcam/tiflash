import pytest

import tiflash

@pytest.mark.usefixtures("device")
class TestXDS110Api():

    def test_basic_xds110reset(self, device):
        """Tests simple xds110reset on each device in devices.cfg"""
        result = tiflash.xds110reset(serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True

    def test_basic_xds110reset_fail(self, device):
        """Tests xds110reset fails when garbage serno used"""
        with pytest.raises(Exception):
            result = tiflash.xds110reset(serno="GARBAGE",
                                connection=device['connection'],
                                devicetype=device['devicetype'])

    def test_basic_xds110list(self, device, t_env):
        """Tests xds110list returns list of all connected devices"""
        devices = t_env['DEVICES'].keys()
        serno_list = [ t_env['DEVICES'][d]['serno'] for d in devices ]

        result = tiflash.xds110list()

        assert len(result) == len(serno_list)

        for serno in serno_list:
            assert serno in result
