import pytest

import tiflash


class TestResetApi:
    def test_basic_reset(self, tdev):
        """Tests simple reset on each device in devices.cfg"""
        result = tiflash.reset(
            serno=tdev["serno"],
            connection=tdev["connection"],
            devicetype=tdev["devicetype"],
        )

        assert result is True
