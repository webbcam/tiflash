import os
import pytest
from tiflash.utils.xds110 import XDS110Error, get_xds110_dir, xds110reset

XDS110_DIRECTORY = "ccs_base/common/uscif/xds110"

class TestXDS110():
    """Test suite for testing xds110 unit"""

    def test_get_xds110_dir(self, t_env):
        ccs_path = t_env['CCS_INSTALLS'][0]
        expected = os.path.abspath(ccs_path + '/' + XDS110_DIRECTORY)

        result = get_xds110_dir(ccs_path)

        assert expected == result

    def test_xds110reset_serno(self, t_env):
        """Calls xds110reset with no serno"""
        ccs_path = t_env['CCS_INSTALLS'][0]
        devices = t_env['DEVICES'].keys()
        device = t_env['DEVICES'][devices[0]]

        if len(devices) == 0:
            pytest.skip("Need devices connected to test xds110reset serno on")

        result = xds110reset(ccs_path, serno=device['serno'])

        assert result == True

    def test_xds110reset_no_serno(self, t_env):
        """Calls xds110reset with no serno"""
        ccs_path = t_env['CCS_INSTALLS'][0]

        result = xds110reset(ccs_path)

        assert result == True

    def test_xds110reset_error(self, t_env):
        """Calls xds110reset on non existant device"""
        ccs_path = t_env['CCS_INSTALLS'][0]
        serno = "LXXXXXX"

        with pytest.raises(XDS110Error):
            result = xds110reset(ccs_path, serno=serno)
