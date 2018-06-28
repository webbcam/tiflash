import shutil
import os

from tiflash.utils import ccxml


class TestCCXML():
    def test_get_ccxml_directory(self, t_env):
        expected = t_env['TARGET_CONFIG_PATH']

        result = ccxml.get_ccxml_directory()

        assert result == expected

    def test_get_serno_from_ccxml(self, t_env):
        # Assuming there already exists a ccxml for first device
        device_key = t_env['DEVICES'].keys()[0]
        device = t_env['DEVICES'][device_key]
        serno = device['serno']

        ccxml_path = os.path.normpath(
            t_env['TARGET_CONFIG_PATH'] + '/%s.ccxml' % serno)
        expected = serno

        result = ccxml.get_serno_from_ccxml(ccxml_path)

        assert result == expected

    def test_add_serno(self, t_env):
        expected = "TEST!!!"
        temp_ccxml = t_env['TEMP_DIR'] + '/NOSERNO.ccxml'
        shutil.copyfile(t_env['RESOURCE_DIR'] + '/no-serno.ccxml', temp_ccxml)
        result = ccxml.add_serno(temp_ccxml, expected, t_env['CCS_INSTALLS'][0])
        assert result is True

        result = ccxml.get_serno_from_ccxml(
            temp_ccxml)    # make this independent
        assert result == expected

    def test_get_connection_xml(self, t_env):
        expected = os.path.normpath(t_env['CCS_INSTALLS'][0] +
                                    "/ccs_base/common/targetdb/connections/"
                                    "TIXDS110_Connection.xml")

        result = ccxml.get_connection_xml(t_env['RESOURCE_DIR'] +
                                          "/cc1350.ccxml",
                                          t_env['CCS_INSTALLS'][0])

        assert result == expected

    def test_get_device_xml(self, t_env):
        # CC1350
        expected = os.path.normpath(t_env['CCS_INSTALLS'][0] +
                                    "/ccs_base/common/targetdb/devices/"
                                    "cc1350f128.xml")

        result = ccxml.get_device_xml(t_env['RESOURCE_DIR'] +
                                      "/cc1350.ccxml", t_env['CCS_INSTALLS'][0])

        assert result == expected

        # CC3220SF
        expected = os.path.normpath(t_env['CCS_INSTALLS'][0] +
                                    "/ccs_base/common/targetdb/devices/"
                                    "CC3220SF.xml")

        result = ccxml.get_device_xml(t_env['RESOURCE_DIR'] +
                                      "/cc3220sf.ccxml",
                                      t_env['CCS_INSTALLS'][0])

        assert result == expected

    def test_get_ccxmls(self, t_env):
        result = ccxml.get_ccxmls()

        for r in result:
            assert r.endswith('.ccxml')
