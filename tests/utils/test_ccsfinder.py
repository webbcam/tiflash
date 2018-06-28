import unittest

from tiflash.utils.ccsfinder import FindCCSError, find_ccs

# List of installed ccs versions (need at least one)
CCS_INSTALLED_VERSIONS = (8, 7)


class TestFindCCS(unittest.TestCase):
    """Test suite for testing ccsfinder unit"""

    def test_ccsfind_latest_version(self):
        ccs_path = find_ccs()
        self.assertIsInstance(ccs_path, str,
                              "Could not find latest ccs installation")

    def test_ccsfind_first_version(self):
        version = CCS_INSTALLED_VERSIONS[0]
        ccs_path = find_ccs(version)
        self.assertIsInstance(ccs_path, str,
                              "Could not find ccs version %d installation"
                              % version)

    @unittest.skipIf(len(CCS_INSTALLED_VERSIONS) < 2,
                     "Need more than one CCS installation to run this test")
    def test_ccsfind_second_version(self):
        version = CCS_INSTALLED_VERSIONS[1]
        ccs_path = find_ccs(version)
        self.assertIsInstance(ccs_path, str,
                              "Could not find ccs version %d installation"
                              % version)

    def test_ccsfind_min_version(self):
        version = min(CCS_INSTALLED_VERSIONS)
        ccs_path = find_ccs(version)
        self.assertIsInstance(ccs_path, str,
                              "Could not find ccs version %d installation"
                              % version)

    def test_ccsfind_missing_installation(self):
        version = max(CCS_INSTALLED_VERSIONS) + 1
        self.assertRaises(FindCCSError, find_ccs, version)

        version = min(CCS_INSTALLED_VERSIONS) - 1
        self.assertRaises(FindCCSError, find_ccs, version)


if __name__ == "__main__":
    unittest.main()
