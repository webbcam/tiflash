import pytest

import tiflash

@pytest.mark.usefixtures("device")
class TestExpressionApi():

    def test_basic_expression(self, device):
        """Runs a simple gel command"""
        EXPRESSION = "MassErase();"
        result = tiflash.evaluate(EXPRESSION,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result == "0"

    def test_invalid_expression_format(self, device):
        """Tries using expression command with invalid C syntax"""

        EXPRESSION = "var i = 0"
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.evaluate(EXPRESSION,
                                serno=device['serno'],
                                connection=device['connection'],
                                devicetype=device['devicetype'])

    def test_expression_with_symbol_load(self, device):
        """Tries using expression command with invalid C syntax"""

        if 'symbol' not in device.keys() or \
            'symbol_image' not in device.keys():
            pytest.skip("No symbol image path or symbol name")

        EXPRESSION = device['symbol']
        SYMBOL_FILE = device['symbol_image']

        result = tiflash.evaluate(EXPRESSION,
                            symbol_file=SYMBOL_FILE,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert result == '0'

