import pytest

import tiflash

class TestRegisterApi():

    def test_basic_register_read(self, tdev):
        """Tests simple register read"""
        REGNAME = "PC"

        result = tiflash.register_read(REGNAME,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert type(result) is int


    def test_basic_register_write(self, tdev):
        """Tests simple register write"""
        REGNAME = "R1"
        VALUE = 0xBEEF

        tiflash.register_write(REGNAME, VALUE,
                        serno=tdev['serno'],
                        connection=tdev['connection'],
                        devicetype=tdev['devicetype'])


    def test_invalid_register_read(self, tdev):
        """Tests an Error is raised when trying to access invalid register for
        register read"""
        INVALID_REGNAME = "INVALIDREGNAME"

        with pytest.raises(tiflash.TIFlashError):
            tiflash.register_read(INVALID_REGNAME,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])


    def test_invalid_register_write(self, tdev):
        """Tests an Error is raised when trying to access invalid register for
        register write"""
        INVALID_REGNAME = "INVALIDPC"
        VALUE = 1

        with pytest.raises(tiflash.TIFlashError):
            tiflash.register_write(INVALID_REGNAME, VALUE,
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])
