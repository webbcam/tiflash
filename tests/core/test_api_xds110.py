import pytest

import tiflash

class TestXDS110Api():

    def test_basic_xds110_reset(self, tdev):
        """Tests simple xds110_reset on each device in devices.cfg"""
        result = tiflash.xds110_reset(serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result is True

    def test_basic_xds110_reset_fail(self, tdev):
        """Tests xds110_reset fails when garbage serno used"""
        with pytest.raises(Exception):
            result = tiflash.xds110_reset(serno="GARBAGE",
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])

    def test_basic_xds110_list(self, tdev, tenv):
        """Tests xds110_list returns list of all connected devices"""
        devices = tenv['devices']
        serno_list = [ tenv[d]['serno'] for d in devices ]

        result = tiflash.xds110_list()
        result_sernos = [ s for (s,v) in result ]

        assert len(result_sernos) == len(serno_list)

        for serno in serno_list:
            assert serno in result_sernos

        #assert tdev['serno'] in result_sernos

    @pytest.mark.skip(reason="Issue with board connections after xds110 upgrade in testing; Please run manually")
    def test_basic_xds110_upgrade(self, tdev):
        """Tests simple xds110_upgrade on each device in devices.cfg"""
        result = tiflash.xds110_upgrade(serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result is True

    def test_basic_xds110_upgrade_fail(self, tdev):
        """Tests xds110_upgrade fails when garbage serno used"""
        with pytest.raises(Exception):
            result = tiflash.xds110_upgrade(serno="GARBAGE",
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])
