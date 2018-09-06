import pytest

import tiflash

@pytest.mark.usefixtures("device")
class TestXDS110Api():

    def test_basic_xds110_reset(self, device):
        """Tests simple xds110_reset on each device in devices.cfg"""
        result = tiflash.xds110_reset(serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True

    def test_basic_xds110_reset_fail(self, device):
        """Tests xds110_reset fails when garbage serno used"""
        with pytest.raises(Exception):
            result = tiflash.xds110_reset(serno="GARBAGE",
                                connection=device['connection'],
                                devicetype=device['devicetype'])

    def test_basic_xds110_list(self, device, t_env):
        """Tests xds110_list returns list of all connected devices"""
        devices = t_env['DEVICES'].keys()
        serno_list = [ t_env['DEVICES'][d]['serno'] for d in devices ]

        result = tiflash.xds110_list()

        assert len(result) == len(serno_list)

        for serno in serno_list:
            assert serno in result

    def test_basic_xds110_upgrade(self, device):
        """Tests simple xds110_upgrade on each device in devices.cfg"""
        result = tiflash.xds110_upgrade(serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True

    def test_basic_xds110_upgrade_fail(self, device):
        """Tests xds110_upgrade fails when garbage serno used"""
        with pytest.raises(Exception):
            result = tiflash.xds110_upgrade(serno="GARBAGE",
                                connection=device['connection'],
                                devicetype=device['devicetype'])
