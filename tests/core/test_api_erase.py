import pytest

from tiflash import core


@pytest.mark.usefixtures("device")
class TestEraseApi():

    def test_basic_erase(self, device):
        """Tests simple erase on each device in devices.cfg"""
        result = core.erase(serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True
