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
        device_key = list(t_env['DEVICES'].keys())[0]
        device = t_env['DEVICES'][device_key]
        serno = device['serno']

        ccxml_path = os.path.normpath(
            t_env['TARGET_CONFIG_PATH'] + '/%s.ccxml' % serno)
        expected = serno

        result = ccxml.get_serno(ccxml_path)

        assert result == expected

    def test_add_serno(self, t_env):
        expected = "TEST!!!"
        temp_ccxml = t_env['TEMP_DIR'] + '/NOSERNO.ccxml'
        shutil.copyfile(t_env['RESOURCE_DIR'] + '/no-serno.ccxml', temp_ccxml)
        result = ccxml.add_serno(temp_ccxml, expected, t_env['CCS_PATH'])
        assert result is True

        result = ccxml.get_serno( temp_ccxml) # make this independent
        assert result == expected

    def test_get_connection_xml(self, t_env):
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    "/ccs_base/common/targetdb/connections/"
                                    "TIXDS110_Connection.xml")

        result = ccxml.get_connection_xml(t_env['RESOURCE_DIR'] +
                                          "/cc1350.ccxml",
                                          t_env['CCS_PATH'])

        assert result == expected

    def test_get_device_xml(self, t_env):
        # CC1350
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    "/ccs_base/common/targetdb/devices/"
                                    "cc1350f128.xml")

        result = ccxml.get_device_xml(t_env['RESOURCE_DIR'] +
                                      "/cc1350.ccxml", t_env['CCS_PATH'])

        assert result == expected

        # CC3220SF
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    "/ccs_base/common/targetdb/devices/"
                                    "CC3220SF.xml")

        result = ccxml.get_device_xml(t_env['RESOURCE_DIR'] +
                                      "/cc3220sf.ccxml",
                                      t_env['CCS_PATH'])

        assert result == expected

    def test_get_ccxmls(self, t_env):
        result = ccxml.get_ccxmls()

        for r in result:
            assert r.endswith('.ccxml')

    def test_no_CCSTargetConfigurations_directory(self, t_env):
        ccxml_dir = ccxml.get_ccxml_directory()
        ccxml_dir_tmp = ccxml_dir + "_temporary"

        # Delete CCXML Directory by renaming it
        os.rename(ccxml_dir, ccxml_dir_tmp)

        # Verify CCXML Directory was removed successfully
        assert os.path.exists(ccxml_dir) is False

        # Calling this should create the CCSTargetConfigurations directory
        ccxml_dir = ccxml.get_ccxml_directory()

        # Verify CCXML Directory was created successfully
        assert os.path.exists(ccxml_dir) is True

        # Restore CCSTargetConfigurations directory
        os.rename(ccxml_dir_tmp, ccxml_dir)
