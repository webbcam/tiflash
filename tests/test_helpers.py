import pytest

from tiflash.core.helpers import (resolve_ccs_path, resolve_ccxml_path, resolve_serno, resolve_devicetype, resolve_connection)


class TestTIFlashHelpers:
    def test_resolve_ccs_path_with_version(self, tenv):
        """Tests resolving a ccs path given a version"""
        for v in tenv["ccs"]["versions"]:
            ccs_path = resolve_ccs_path(v)
            assert ccs_path == tenv["ccs"][v]

    def test_resolve_ccs_path_with_ccs_path(self, tenv):
        """Tests resolving a ccs path given a version"""
        for v in tenv["ccs"]["versions"]:
            ccs_path = resolve_ccs_path(tenv["ccs"][v])
            assert ccs_path == tenv["ccs"][v]

    def test_resolve_ccs_path_with_ccs_prefix(self, tenv):
        """Tests resolving a ccs path given a version"""
        ccs_installations = [tenv["ccs"][v] for v in tenv["ccs"]["versions"]]
        ccs_path = resolve_ccs_path(tenv["ccs"]["prefix"])
        assert ccs_path in ccs_installations

    def test_resolve_ccxml_path_with_ccxml(self, tdev):
        """Tests ccxml is able to be found when providing the path"""
        ccxml_path = tdev['ccxml-path']

        assert ccxml_path == resolve_ccxml_path(ccxml=ccxml_path)

    def test_resolve_ccxml_path_with_serno(self, tenv, tdev):
        """Tests ccxml is able to be found when providing the serno"""
        ccxml_path = tenv["paths"]["ccxml"]+"/"+tdev["serno"]+".ccxml"

        assert ccxml_path == resolve_ccxml_path(serno=tdev['serno'])

    def test_resolve_ccxml_path_with_devicetype(self, tenv, tdev):
        """Tests ccxml is able to be found when providing the devicetype"""
        ccxml_path = tenv["paths"]["ccxml"]+"/"+tdev["devicetype"]+".ccxml"

        assert ccxml_path == resolve_ccxml_path(devicetype=tdev['devicetype'])

    def test_resolve_ccxml_path_fails_no_args(self, tdev):
        """Tests exception raised when no args are provided"""
        with pytest.raises(Exception):
            assert ccxml_path == resolve_ccxml_path()

    def test_resolve_ccxml_path_fails_invalid_ccxml_path(self, tdev):
        """Tests exception raised when not able to find ccxml from path"""
        ccxml_path = "/path/to/invalid.ccxml"
        with pytest.raises(Exception):
            ccxml_path == resolve_ccxml_path(ccxml=ccxml_path)

    def test_resolve_ccxml_path_fails_invalid_serno(self, tdev):
        """Tests exception raised when not able to find ccxml from serno"""
        serno = "INAVLID_SERNO"
        with pytest.raises(Exception):
            ccxml_path == resolve_ccxml_path(serno=serno)

    def test_resolve_ccxml_path_fails_invalid_devicetype(self, tdev):
        """Tests exception raised when not able to find ccxml from devicetype"""
        devicetype = "INVALID_DEVICETYPE"
        with pytest.raises(Exception):
            ccxml_path == resolve_ccxml_path(devicetype=devicetype)

    def test_resolve_serno_with_serno(self, tenv, tdev):
        """Tests serno is able to be resolved when providing the serno"""
        assert tdev['serno'] == resolve_serno(serno=tdev['serno'])

    def test_resolve_serno_with_ccxml(self, tenv, tdev):
        """Tests serno is able to be resolved when providing the ccxml"""
        ccxml_path = tdev['ccxml-path']

        assert tdev['serno'] == resolve_serno(ccxml=ccxml_path)

    def test_resolve_serno_fails_no_args(self, tdev):
        """Tests exception raised when no args are provided"""
        with pytest.raises(Exception):
            resolve_serno()

    def test_resolve_devicetype_with_devicetype(self, tenv, tdev):
        """Tests devicetype is able to be resolved when providing the devicetype"""
        assert tdev['devicetype'] == resolve_devicetype(devicetype=tdev['devicetype'], ccs_path=tenv['paths']['ccs'])

    def test_resolve_devicetype_with_serno(self, tenv, tdev):
        """Tests devicetype is able to be resolved when providing the serno"""
        assert tdev['devicetype'] == resolve_devicetype(serno=tdev['serno'], ccs_path=tenv['paths']['ccs'])

    def test_resolve_devicetype_with_ccxml(self, tenv, tdev):
        """Tests devicetype is able to be resolved when providing the ccxml"""
        ccxml_path = tdev['ccxml-path']

        assert tdev['devicetype'] == resolve_devicetype(ccxml=ccxml_path, ccs_path=tenv['paths']['ccs'])

    def test_resolve_devicetype_fails_no_args(self, tdev):
        """Tests exception raised when no args are provided"""
        with pytest.raises(Exception):
            resolve_devicetype()

    def test_resolve_connection_with_connection(self, tenv, tdev):
        """Tests connection is able to be resolved when providing the connection"""
        assert tdev['connection'] == resolve_connection(connection=tdev['connection'], ccs_path=tenv['paths']['ccs'])

    def test_resolve_connection_with_ccxml(self, tenv, tdev):
        """Tests connection is able to be resolved when providing the ccxml"""
        ccxml_path = tdev['ccxml-path']

        assert tdev['connection'] == resolve_connection(ccxml=ccxml_path, ccs_path=tenv['paths']['ccs'])

    def test_resolve_connection_with_devicetype(self, tenv, tdev):
        """Tests connection is able to be resolved when providing the devicetype"""
        assert tdev['connection'] == resolve_connection(devicetype=tdev['devicetype'], ccs_path=tenv['paths']['ccs'])

    def test_resolve_connection_fails_no_args(self, tdev):
        """Tests exception raised when no args are provided"""
        with pytest.raises(Exception):
            resolve_connection()

