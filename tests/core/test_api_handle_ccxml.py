# import pytest

# from tiflash import core, TIFlashError
import tiflash


class TestHandleCCXML():

    # Providing Serno
    def test_serno_ccxml_no_exist(self, tdev):
        pass

    def test_serno_ccxml_no_exist_fresh(self, tdev):
        pass

    def test_serno_ccxml_exist(self, tdev):
        pass

    def test_serno_ccxml_exist_fresh(self, tdev):
        pass

    def test_serno_ccxml_exist_fresh_connection_provided(self, tdev):
        pass

    def test_serno_ccxml_exist_fresh_device_provided(self, tdev):
        pass

    def test_serno_ccxml_exist_fresh_connection_device_provided(self, tdev):
        pass

    def test_serno_ccxml_exist_connection_override(self, tdev):
        pass

    def test_serno_ccxml_exist_device_override(self, tdev):
        pass

    def test_serno_ccxml_exist_connection_device_override(self, tdev):
        pass

    # Providing CCXML
    def test_ccxml_basic(self, tdev):
        pass

    def test_ccxml_basic_fresh(self, tdev):
        pass

    def test_ccxml_fresh_connection_override(self, tdev):
        pass

    def test_ccxml_fresh_device_override(self, tdev):
        pass

    def test_ccxml_fresh_device_connection_override(self, tdev):
        pass

    def test_ccxml_no_exist(self, tdev):
        pass

    # duplicate
    def test_ccxml_connection_override(self, tdev):
        pass

    # duplicate
    def test_ccxml_device_override(self, tdev):
        pass

    # duplicate
    def test_ccxml_device_connection_override(self, tdev):
        pass

    # Raise Error
    def test_connection_only_provided(self):
        pass

    def test_bad_serno(self):
        pass

    # Weird Cases
    def test_bad_serno_but_connection_device_provided(self):
        pass
