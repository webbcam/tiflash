import sys


class TestAPIInstaller:
    def test_import(self):
        """Tests tiflash can be imported"""
        import tiflash

        assert "tiflash" in sys.modules.keys()
