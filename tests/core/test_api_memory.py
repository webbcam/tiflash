import pytest

import tiflash

class TestMemoryApi():

    def test_basic_memory_read_single_byte(self, tdev):
        """Tests simple memory read"""
        result = tiflash.memory_read(tdev['address'], 1,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert len(result) == 1

    def test_basic_memory_read_multiple_bytes(self, tdev):
        """Tests simple memory read of multiple bytes"""
        result = tiflash.memory_read(tdev['address'], 4,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert len(result) == 4

    def test_basic_memory_read_and_check_byte_values(self, tdev):
        """Tests memory read and checks for correct byte values. This test is
        device specific."""

        if "address" not in tdev.keys() or \
            "value" not in tdev.keys():
            pytest.skip("Need to add memval and memaddr fields in \
                setup.cfg for device: %s" % tdev['devicetype'])

        addr = int(tdev['address'], 0)
        answer = tdev['value'].split(',')
        answer = [ int(d, 0) for d in answer ]
        result = tiflash.memory_read(addr, len(answer),
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert len(result) == len(answer)
        assert result == answer


    def test_basic_memory_write(self, tdev):
        """Tests simple memory write"""
        WRITE_DATA = [0x11, 0x22, 0x33]
        tiflash.memory_write(tdev['address'], WRITE_DATA,
                        serno=tdev['serno'],
                        connection=tdev['connection'],
                        devicetype=tdev['devicetype'])


    def test_invalid_address_memory_read(self, tdev):
        """Tests an Error is raised when trying to access invalid memory for
        memory read"""
        INVALID_ADDRESS = 0xFFFFFFFF
        NUM_BYTES = 4

        with pytest.raises(tiflash.TIFlashError):
            tiflash.memory_read(INVALID_ADDRESS, NUM_BYTES,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])


    def test_invalid_address_memory_write(self, tdev):
        """Tests an Error is raised when trying to access invalid memory for
        memory write"""
        INVALID_ADDRESS = 0x10000000
        WRITE_DATA = [0x11, 0x22, 0x33]

        with pytest.raises(tiflash.TIFlashError):
            tiflash.memory_write(INVALID_ADDRESS, WRITE_DATA,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])
