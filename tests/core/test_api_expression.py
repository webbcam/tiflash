import pytest

import tiflash

class TestExpressionApi():

    def test_basic_expression(self, tdev):
        """Runs a simple gel command"""
        result = tiflash.evaluate(tdev['expression'],
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        assert result == "0"

    def test_invalid_expression_format(self, tdev):
        """Tries using expression command with invalid C syntax"""

        EXPRESSION = "var i = 0"
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.evaluate(EXPRESSION,
                                serno=tdev['serno'],
                                connection=tdev['connection'],
                                devicetype=tdev['devicetype'])

    def test_expression_with_symbol_load(self, tdev):
        """Tries using expression command with invalid C syntax"""

        if 'symbol' not in tdev.keys() or \
            'symbol-image' not in tdev.keys():
            pytest.skip("No symbol image path or symbol name")

        result = tiflash.evaluate(tdev['symbol'],
                            symbol_file=tdev['symbol-image'],
                            serno=tdev['serno'],
                            connection=tdev['connection'],
                            devicetype=tdev['devicetype'])

        #assert result == '0'

