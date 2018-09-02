import pytest
from tiflash.utils.ccs import FindCCSError, find_ccs, get_workspace_dir

class TestCCS():
    """Test suite for testing ccsfinder unit"""

    def test_ccsfind_first_version(self, t_env):
        version = t_env['CCS_VERSIONS'][0]
        ccs_path = find_ccs(version)
        assert isinstance(ccs_path, str), \
                              "Could not find ccs version %d installation" \
                              % version

    def test_ccsfind_second_version(self, t_env):
        if len(t_env['CCS_VERSIONS']) < 2:
            pytest.skip("Need more than one CCS installation to run this test")

        version = t_env['CCS_VERSIONS'][1]
        ccs_path = find_ccs(version)
        assert isinstance(ccs_path, str), \
                              "Could not find ccs version %d installation" \
                              % version

    def test_ccsfind_latest_version(self, t_env):
        latest_ccs_path = find_ccs()
        version = max(t_env['CCS_VERSIONS'])
        max_ccs_path = find_ccs(version)

        assert (latest_ccs_path == max_ccs_path)


    def test_ccsfind_min_version(self, t_env):
        version = min(t_env['CCS_VERSIONS'])
        ccs_path = find_ccs(version)
        assert isinstance(ccs_path, str), \
                              "Could not find ccs version %d installation" \
                              % version


    def test_ccsfind_missing_installation(self, t_env):
        version = max(t_env['CCS_VERSIONS']) + 1
        with pytest.raises(FindCCSError):
            find_ccs(version)

        version = min(t_env['CCS_VERSIONS']) - 1
        with pytest.raises(FindCCSError):
            find_ccs(version)


    def test_get_workspace_dir(self, t_env):
        answer = "@user.home/workspace_tiflash"

        assert get_workspace_dir() == answer

