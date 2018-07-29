import pytest

from tiflash import core, TIFlashError

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

    def test_basic_memory_read_and_check_byte_values(self, device):
        """Tests memory read and checks for correct byte values. This test is
        device specific."""

        if "memaddr" not in device.keys() or \
            "memval" not in device.keys():
            pytest.skip("Need to add memval and memaddr fields in \
                setup.cfg for device: %s" % device['devicetype'])

        addr = int(device['memaddr'], 0)
        answer = device['memval'].split(',')
        answer = [ int(d, 0) for d in answer ]
        result = core.memory_read(addr, len(answer),
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert len(result) == len(answer)
        assert result == answer


    def test_basic_memory_write(self, device):
        """Tests simple memory write"""
        WRITE_ADDRESS = 0x20000000
        WRITE_DATA = [0x11, 0x22, 0x33]
        core.memory_write(WRITE_ADDRESS, WRITE_DATA,
                        serno=device['serno'],
                        connection=device['connection'],
                        devicetype=device['devicetype'])


    def test_invalid_address_memory_read(self, device):
        """Tests an Error is raised when trying to access invalid memory for
        memory read"""
        INVALID_ADDRESS = 0xFFFFFFFF
        NUM_BYTES = 4

        with pytest.raises(TIFlashError):
            core.memory_read(INVALID_ADDRESS, NUM_BYTES,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])


    def test_invalid_address_memory_write(self, device):
        """Tests an Error is raised when trying to access invalid memory for
        memory write"""
        INVALID_ADDRESS = 0x10000000
        WRITE_DATA = [0x11, 0x22, 0x33]

        with pytest.raises(TIFlashError):
            core.memory_write(INVALID_ADDRESS, WRITE_DATA,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])
