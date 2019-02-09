import os
import pytest
from tiflash.utils.ccs import FindCCSError, find_ccs, get_workspace_dir, get_ccs_version

class TestCCS():
    """Test suite for testing ccsfinder unit"""

    def test_ccsfind_first_version(self, t_env):
        version = t_env['CCS_VERSIONS'][0]
        ccs_path = find_ccs(version=version)
        assert isinstance(ccs_path, str), \
                              "Could not find ccs version %d installation" \
                              % version

    def test_ccsfind_second_version(self, t_env):
        if len(t_env['CCS_VERSIONS']) < 2:
            pytest.skip("Need more than one CCS installation to run this test")

        version = t_env['CCS_VERSIONS'][1]
        ccs_path = find_ccs(version=version)
        assert isinstance(ccs_path, str), \
                              "Could not find ccs version %s installation" \
                              % version

    def test_ccsfind_latest_version(self, t_env):
        latest_ccs_path = find_ccs()
        version = max(t_env['CCS_VERSIONS'])
        max_ccs_path = find_ccs(version=version)

        assert (latest_ccs_path == max_ccs_path)


    def test_ccsfind_min_version(self, t_env):
        version = min(t_env['CCS_VERSIONS'])
        ccs_path = find_ccs(version=version)
        assert isinstance(ccs_path, str), \
                              "Could not find ccs version %d installation" \
                              % version


    def test_ccsfind_missing_installation(self, t_env):
        version = "0.0.0.00009"
        with pytest.raises(Exception):
            find_ccs(version=version)

    def test_get_workspace_dir(self, t_env):
        answer = "@user.home/.tiflash/workspace"

        assert get_workspace_dir() == answer

    def test_get_ccs_version_from_path(self, t_env):
        answer = t_env['CCS_VERSIONS'][0]

        path = find_ccs(version=answer)

        result = get_ccs_version(path)

        assert result == answer

    def test_ccsfind_nonexistant_custom_install_using_ccs_prefix_param(self, t_env):
        ccs_prefix = "/nonexistant/path/to/ccs"
        with pytest.raises(Exception):
            ccs_path = find_ccs(ccs_prefix=ccs_prefix)

    def test_ccsfind_nonexistant_custom_install_using_env_var(self, t_env):
        os.environ['CCS_PREFIX'] = "/nonexistant/path/to/ccs"
        with pytest.raises(Exception):
            ccs_path = find_ccs()
