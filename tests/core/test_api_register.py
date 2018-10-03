import pytest

import tiflash

@pytest.mark.usefixtures("device")
class TestRegisterApi():

    def test_basic_register_read(self, device):
        """Tests simple register read"""
        REGNAME = "PC"

        result = tiflash.register_read(REGNAME,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert type(result) is int


    def test_basic_register_write(self, device):
        """Tests simple register write"""
        REGNAME = "R1"
        VALUE = 0xBEEF

        tiflash.register_write(REGNAME, VALUE,
                        serno=device['serno'],
                        connection=device['connection'],
                        devicetype=device['devicetype'])


    def test_invalid_register_read(self, device):
        """Tests an Error is raised when trying to access invalid register for
        register read"""
        INVALID_REGNAME = "INVALIDREGNAME"

        with pytest.raises(tiflash.TIFlashError):
            tiflash.register_read(INVALID_REGNAME,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])


    def test_invalid_register_write(self, device):
        """Tests an Error is raised when trying to access invalid register for
        register write"""
        INVALID_REGNAME = "PC"
        VALUE = 1

        with pytest.raises(tiflash.TIFlashError):
            tiflash.register_write(INVALID_REGNAME, VALUE,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])
