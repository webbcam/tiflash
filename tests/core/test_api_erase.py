import pytest

import tiflash


class TestEraseApi():

    def test_basic_erase(self, tdev):
        """Tests simple erase on each device in devices.cfg"""
        result = tiflash.erase(serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result is True
