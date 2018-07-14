import pytest

from tiflash import core


@pytest.mark.usefixtures("device")
class TestResetApi():

    def test_basic_reset(self, device):
        """Tests simple reset on each device in devices.cfg"""
        result = core.reset(serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result is True
