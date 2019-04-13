import os
import pytest

from tiflash.utils import devices


class TestDevices():
    def test_get_devices_directory(self, tenv):
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    '/ccs_base/common/targetdb/devices')

        result = devices.get_devices_directory(tenv['paths']['ccs'])

        assert result == expected

    def test_get_devicetypes(self, tenv):
        result = devices.get_devicetypes(tenv['paths']['ccs'])

        assert type(result) is list

    def test_get_devicetype(self, tenv):
        expected = "CC1350F128"
        devicexml = os.path.normpath(tenv['paths']['ccs'] +
                                     "/ccs_base/common/targetdb/devices"
                                     "/cc1350f128.xml")

        result = devices.get_devicetype(devicexml)

        assert result == expected

    def test_get_cpu_xml(self, tenv):
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    "/ccs_base/common/targetdb/cpus/"
                                    "cortex_m3.xml")

        device_xml = os.path.normpath(tenv['paths']['ccs'] +
                                      "/ccs_base/common/targetdb/devices/"
                                      "cc1350f128.xml")

        result = devices.get_cpu_xml(device_xml, tenv['paths']['ccs'])

        assert result == expected

    def test_get_default_connection_xml(self, tenv):
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    "/ccs_base/common/targetdb/connections/"
                                    "TIXDS110_Connection.xml")

        device_xml = os.path.normpath(tenv['paths']['ccs'] +
                                      "/ccs_base/common/targetdb/devices/"
                                      "cc1350f128.xml")

        result = devices.get_default_connection_xml(device_xml,
                                                    tenv['paths']['ccs'])

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
    def test_get_device_from_serno(self, tenv, serno, expected):

        result = devices.get_device_from_serno(serno, tenv['paths']['ccs'])

        assert result == expected
