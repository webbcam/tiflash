import pytest
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
