# import pytest

# from tiflash import core, TIFlashError


class TestHandleCCXML():

    # Providing Serno
    def test_serno_ccxml_no_exist(self, device):
        pass

    def test_serno_ccxml_no_exist_fresh(self, device):
        pass

    def test_serno_ccxml_exist(self, device):
        pass

    def test_serno_ccxml_exist_fresh(self, device):
        pass

    def test_serno_ccxml_exist_fresh_connection_provided(self, device):
        pass

    def test_serno_ccxml_exist_fresh_device_provided(self, device):
        pass

    def test_serno_ccxml_exist_fresh_connection_device_provided(self, device):
        pass

    def test_serno_ccxml_exist_connection_override(self, device):
        pass

    def test_serno_ccxml_exist_device_override(self, device):
        pass

    def test_serno_ccxml_exist_connection_device_override(self, device):
        pass

    # Providing CCXML
    def test_ccxml_basic(self, device):
        pass

    def test_ccxml_basic_fresh(self, device):
        pass

    def test_ccxml_fresh_connection_override(self, device):
        pass

    def test_ccxml_fresh_device_override(self, device):
        pass

    def test_ccxml_fresh_device_connection_override(self, device):
        pass

    def test_ccxml_no_exist(self, device):
        pass

    # duplicate
    def test_ccxml_connection_override(self, device):
        pass

    # duplicate
    def test_ccxml_device_override(self, device):
        pass

    # duplicate
    def test_ccxml_device_connection_override(self, device):
        pass

    # Raise Error
    def test_connection_only_provided(self):
        pass

    def test_bad_serno(self):
        pass

    # Weird Cases
    def test_bad_serno_but_connection_device_provided(self):
        pass
