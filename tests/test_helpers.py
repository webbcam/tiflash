import pytest

from tiflash.core.helpers import resolve_ccs_path


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
