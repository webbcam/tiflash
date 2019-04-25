import pytest
import shutil
import tiflash


class TestTIFlashSession:
    def test_instantiation(self):
        """Tests basic instantation of TIFlashSession object with no parameters"""
        device = tiflash.TIFlashSession()

    def test_instantiation_with_deprecated_ccs_path(self, tenv):
        """Tests basic instantation of TIFlashSession object with provided ccs path"""
        ccs_path = tenv["paths"]["ccs"]
        device = tiflash.TIFlashSession(ccs=ccs_path)

    def test_instantiation_with_deprecated_ccs_version(self, tenv):
        """Tests basic instantation of TIFlashSession object with provided ccs path"""
        ccs_version = tenv["ccs"]["versions"][0]
        device = tiflash.TIFlashSession(ccs=ccs_version)

    def test_instantiation_with_ccs_path(self, tenv):
        """Tests basic instantation of TIFlashSession object with provided ccs path"""
        ccs_path = tenv["paths"]["ccs"]
        device = tiflash.TIFlashSession(ccs_path=ccs_path)

    def test_instantiation_with_ccs_version(self, tenv):
        """Tests basic instantation of TIFlashSession object with provided ccs path"""
        ccs_version = tenv["ccs"]["versions"][0]
        device = tiflash.TIFlashSession(ccs_version=ccs_version)

    def test_instantiation_with_ccs_prefix_and_version(self, tenv):
        """Tests basic instantation of TIFlashSession object with provided ccs path"""
        ccs_version = tenv["ccs"]["versions"][0]
        ccs_prefix = tenv["ccs"]["prefix"]
        device = tiflash.TIFlashSession(ccs_path=ccs_prefix, ccs_version=ccs_version)

    def test_instantiation_with_device_params(self, tenv, tdev):
        """Tests basic instantation of TIFlashSession object with provided device params"""
        serno = tdev.get('serno', None)
        devicetype = tdev.get('devicetype', None)
        connection = tdev.get('connection', None)
        device = tiflash.TIFlashSession(serno=serno, devicetype=devicetype, connection=connection)

    def test_instantiation_with_ccxml(self, tenv, tdev):
        """Tests basic instantation of TIFlashSession object with provided device params"""
        ccxml = tdev['ccxml-path']
        device = tiflash.TIFlashSession(ccxml=ccxml)

        assert device.ccxml_path == ccxml

        if 'serno' in tdev.keys():
            assert device.serno == tdev['serno']
        assert device.devicetype == tdev['devicetype']
        assert device.connection == tdev['connection']

    def test_instantiation_with_ccxml_new_serno(self, tenv, tdev):
        """Tests basic instantation of TIFlashSession object with provided ccxml and different serno"""
        if 'serno' not in tdev.keys():
            pytest.skip("Device %s has no serial number" % tdev["devicetype"])

        ccxml = tenv["paths"]["tmp"]+"/"+tdev["serno"]+".ccxml"
        serno = "NEW_SERNO"

        # Going to be altering the ccxml file so making a copy to modify
        shutil.copyfile(tdev["ccxml-path"], ccxml)

        device = tiflash.TIFlashSession(serno=serno, ccxml=ccxml)

        assert device.ccxml_path == ccxml
        assert device.serno != tdev['serno']
        assert device.serno == serno
        assert device.devicetype == tdev['devicetype']
        assert device.connection == tdev['connection']

        # Check the new serial number was updated on the provided ccxml file
        with open(ccxml) as f:
            text = f.read()
            assert serno in text
            assert tdev['serno'] not in text
