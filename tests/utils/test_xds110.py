import os
import pytest
from tiflash.utils.xds110 import (XDS110Error, get_xds110_dir,
                                get_xds110_exe_path, xds110_upgrade,
                                xds110_reset, xds110_list)

XDS110_DIRECTORY = "ccs_base/common/uscif/xds110"

class TestXDS110():
    """Test suite for testing xds110 unit"""

    def test_get_xds110_dir(self, tenv):
        ccs_path = tenv['paths']['ccs']
        expected = os.path.abspath(ccs_path + '/' + XDS110_DIRECTORY)

        result = get_xds110_dir(ccs_path)

        assert expected == result

    def test_get_xds110_exe_path(self, tenv):
        ccs_path = tenv['paths']['ccs']
        expected = os.path.abspath(ccs_path + '/' + XDS110_DIRECTORY
                                    + '/' + 'xdsdfu')

        result = get_xds110_exe_path(ccs_path, 'xdsdfu')

        assert expected == result

    def test_xds110_reset_serno(self, tenv):
        """Calls xds110_reset with serno"""
        ccs_path = tenv['paths']['ccs']
        devices = tenv['devices']
        device = tenv[devices[0]]

        if len(devices) == 0:
            pytest.skip("Need devices connected to test xds110_reset serno on")

        result = xds110_reset(ccs_path, serno=device['serno'])

        assert result == True

    def test_xds110_reset_no_serno(self, tenv):
        """Calls xds110_reset with no serno"""
        ccs_path = tenv['paths']['ccs']

        result = xds110_reset(ccs_path)

        assert result == True

    def test_xds110_reset_error(self, tenv):
        """Calls xds110_reset on non existant device"""
        ccs_path = tenv['paths']['ccs']
        serno = "GARBAGE"

        with pytest.raises(XDS110Error):
            result = xds110_reset(ccs_path, serno=serno)

    def test_xds110_list(self, tenv):
        """Calls xds110_list and checks connected all devices are returned"""
        ccs_path = tenv['paths']['ccs']
        devices = tenv['devices']
        serno_list = [ tenv[d]['serno'] for d in devices ]

        result = xds110_list(ccs_path)

        assert len(result) == len(serno_list)

        for serno in serno_list:
            assert serno in [ s for (s,_) in result ]

    #@pytest.mark.skip(reason="Issue with board connections after xds110 upgrade in testing; Please run manually")
    def test_xds110_upgrade(self, tenv):
        """Calls xds110_upgrade with serno"""
        ccs_path = tenv['paths']['ccs']
        devices = tenv['devices']
        device = tenv[devices[0]]

        if len(devices) == 0:
            pytest.skip("Need devices connected to test xds110_reset serno on")

        result = xds110_upgrade(ccs_path, serno=device['serno'])

        assert result == True

    @pytest.mark.skip(reason="Issue with board connections after xds110 upgrade in testing; Please run manually")
    def test_xds110_upgrade_no_serno(self, tenv):
        """Calls xds110_upgrade with no serno"""
        ccs_path = tenv['paths']['ccs']

        result = xds110_upgrade(ccs_path)

        assert result == True

    def test_xds110_upgrade_error(self, tenv):
        """Calls xds110_upgrade on non existant device"""
        ccs_path = tenv['paths']['ccs']
        serno = "GARBAGE"

        with pytest.raises(XDS110Error):
            result = xds110_upgrade(ccs_path, serno=serno)
