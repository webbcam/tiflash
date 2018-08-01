import pytest

from tiflash import core, TIFlashError

@pytest.mark.usefixtures("device")
class TestExpressionApi():

    def test_basic_expression(self, device):
        """Runs a simple gel command"""
        EXPRESSION = "mass_erase();"
        result = core.expression(EXPRESSION,
                            serno=device['serno'],
                            connection=device['connection'],
                            devicetype=device['devicetype'])

        assert len(result) == "true"

    def test_invalid_expression_format(self, device):
        """Tries using expression command with invalid C syntax"""

        EXPRESSION = "var i = 0"
        with pytest.raises(TIFlashError):
            result = core.expression(EXPRESSION,
                                serno=device['serno'],
                                connection=device['connection'],
                                devicetype=device['devicetype'])
