import shutil
import os

from tiflash.utils import ccxml


class TestCCXML():
    def test_get_ccxml_directory(self, tenv):
        expected = tenv['paths']['ccxml']

        result = ccxml.get_ccxml_directory()

        assert result == expected

    def test_get_serno_from_ccxml(self, tenv):
        # Assuming there already exists a ccxml for first device
        device_key = tenv['devices'][0]
        device = tenv[device_key]
        serno = device['serno']

        ccxml_path = os.path.normpath(
            tenv['paths']['ccxml'] + '/%s.ccxml' % serno)
        expected = serno

        result = ccxml.get_serno(ccxml_path)

        assert result == expected

    def test_add_serno(self, tenv):
        expected = "TEST!!!"
        temp_ccxml = tenv['paths']['tmp'] + '/NOSERNO.ccxml'
        shutil.copyfile(tenv['paths']['resources'] + '/no-serno.ccxml', temp_ccxml)
        result = ccxml.add_serno(temp_ccxml, expected, tenv['paths']['ccs'])
        assert result is True

        result = ccxml.get_serno( temp_ccxml) # make this independent
        assert result == expected

    def test_get_connection_xml(self, tenv, tdev):
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    "/ccs_base/common/targetdb/connections/"
                                    "TIXDS110_Connection.xml")

        result = ccxml.get_connection_xml(tdev['ccxml-path'],
                                          tenv['paths']['ccs'])

        assert result == expected

    def test_get_device_xml(self, tenv, tdev):
        # CC1350
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    "/ccs_base/common/targetdb/devices/"
                                    "cc1310f128.xml")

        result = ccxml.get_device_xml(tdev['ccxml-path'],
                                      tenv['paths']['ccs'])

        assert result == expected

        # CC3220SF
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    "/ccs_base/common/targetdb/devices/"
                                    "CC3220SF.xml")

        result = ccxml.get_device_xml(tenv['paths']['resources'] +
                                      "/cc3220sf.ccxml",
                                      tenv['paths']['ccs'])

        assert result == expected

    def test_get_ccxmls(self, tenv):
        result = ccxml.get_ccxmls()

        for r in result:
            assert r.endswith('.ccxml')

    def test_no_CCSTargetConfigurations_directory(self, tenv):
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
