import os
import pytest

from tiflash.utils import devices


class TestDevices():
    def test_get_devices_directory(self, t_env):
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    '/ccs_base/common/targetdb/devices')

        result = devices.get_devices_directory(t_env['CCS_PATH'])

        assert result == expected

    def test_get_devices(self, t_env):
        result = devices.get_devices(t_env['CCS_PATH'])

        assert type(result) is list

    def test_get_device_name(self, t_env):
        expected = "CC1350F128"
        devicexml = os.path.normpath(t_env['CCS_PATH'] +
                                     "/ccs_base/common/targetdb/devices"
                                     "/cc1350f128.xml")

        result = devices.get_device_name(devicexml)

        assert result == expected

    def test_get_cpu_xml(self, t_env):
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    "/ccs_base/common/targetdb/cpus/"
                                    "cortex_m3.xml")

        device_xml = os.path.normpath(t_env['CCS_PATH'] +
                                      "/ccs_base/common/targetdb/devices/"
                                      "cc1350f128.xml")

        result = devices.get_cpu_xml(device_xml, t_env['CCS_PATH'])

        assert result == expected

    def test_get_default_connection_xml(self, t_env):
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    "/ccs_base/common/targetdb/connections/"
                                    "TIXDS110_Connection.xml")

        device_xml = os.path.normpath(t_env['CCS_PATH'] +
                                      "/ccs_base/common/targetdb/devices/"
                                      "cc1350f128.xml")

        result = devices.get_default_connection_xml(device_xml,
                                                    t_env['CCS_PATH'])

        assert result == expected

    @pytest.mark.parametrize("serno,expected", [
        ("L100", "CC2650F128"),
        ("L110", "CC2652R1F"),
        ("L200", "CC1310F128"),
        ("L210", "CC1312R1F3"),
        ("L201", "CC1310F128"),
        ("L400", "CC1350F128"),
        ("L401", "CC1350F128"),
        ("L410", "CC1352R1F3"),
        ("L420", "CC1352P1F3"),
    ])
    def test_get_device_by_serno(self, t_env, serno, expected):

        result = devices.get_device_by_serno(serno, t_env['CCS_PATH'])

        assert result == expected
