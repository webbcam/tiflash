import os
import pytest
from tiflash.utils.ccs import (
    FindCCSError,
    find_ccs,
    get_workspace_dir,
    get_ccs_version,
    get_unique_workspace,
)


class TestCCS:
    """Test suite for testing ccsfinder unit"""

    def test_ccsfind_first_version(self, tenv):
        version = tenv["ccs"]["versions"][0]
        ccs_path = find_ccs(version=version)
        assert isinstance(ccs_path, str), (
            "Could not find ccs version %d installation" % version
        )

    def test_ccsfind_second_version(self, tenv):
        if len(tenv["ccs"]["versions"]) < 2:
            pytest.skip("Need more than one CCS installation to run this test")

        version = tenv["ccs"]["versions"][1]
        ccs_path = find_ccs(version=version)
        assert isinstance(ccs_path, str), (
            "Could not find ccs version %s installation" % version
        )

    def test_ccsfind_latest_version(self, tenv):
        latest_ccs_path = find_ccs()
        version = max(tenv["ccs"]["versions"])
        max_ccs_path = find_ccs(version=version)

        assert latest_ccs_path == max_ccs_path

    def test_ccsfind_min_version(self, tenv):
        version = min(tenv["ccs"]["versions"])
        ccs_path = find_ccs(version=version)
        assert isinstance(ccs_path, str), (
            "Could not find ccs version %d installation" % version
        )

    def test_ccsfind_missing_installation(self, tenv):
        version = "0.0.0.00009"
        with pytest.raises(Exception):
            find_ccs(version=version)

    def test_get_workspace_dir(self, tenv):
        answer = os.path.expanduser("~/.tiflash/workspace")

        assert get_workspace_dir() == answer

    def test_get_unique_workspace(self, tenv):
        answer = os.path.expanduser("~/.tiflash/workspace")

        assert get_unique_workspace() != get_unique_workspace()

    def test_get_ccs_version_from_path(self, tenv):
        answer = tenv["ccs"]["versions"][0]

        path = find_ccs(version=answer)

        result = get_ccs_version(path)

        assert result == answer

    def test_ccsfind_nonexistant_custom_install_using_ccs_prefix_param(self, tenv):
        ccs_prefix = "/nonexistant/path/to/ccs"
        with pytest.raises(Exception):
            ccs_path = find_ccs(ccs_prefix=ccs_prefix)

    def test_ccsfind_nonexistant_custom_install_using_env_var(self, tenv):
        os.environ["CCS_PREFIX"] = "/nonexistant/path/to/ccs"
        with pytest.raises(Exception):
            ccs_path = find_ccs()
