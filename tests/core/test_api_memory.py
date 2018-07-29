import pytest

from tiflash import core

ADDRESS = 0x500012F0
ANSWER = [0xFF, 0xFF, 0xFF, 0xFF]


@pytest.mark.usefixtures("device")
class TestMemoryApi():

    def test_basic_memory_read_single_byte(self, device):
        """Tests simple memory read"""
        result = core.memory_read(ADDRESS, 1,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert len(result) == 1

    def test_basic_memory_read_multiple_bytes(self, device):
        """Tests simple memory read of multiple bytes"""
        result = core.memory_read(ADDRESS, 4,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert len(result) == 4

    @pytest.skip
    def test_basic_memory_write(self, device):
        """Tests simple memory write"""
        result = core.memory_write(ADDRESS, ANSWER,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

    def test_invalid_address_memory_read(self, device):
        """Tests an Error is raised when trying to access invalid memory for
        memory read"""
        pass

    def test_invalid_address_memory_write(self, device):
        """Tests an Error is raised when trying to access invalid memory for
        memory write"""
        pass
