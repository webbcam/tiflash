import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

@pytest.mark.usefixtures("device")
class TestExpressionCli():

    def test_basic_expression(self, device):
        """Runs a simple gel command"""
        EXPRESSION = "MassErase();"

        cmd = get_cmd_with_device_params(device)

        cmd.extend(["evaluate", "\"%s\"" % EXPRESSION])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_invalid_expression_format(self, device):
        """Tries using expression command with invalid C syntax"""

        EXPRESSION = "var i = 0"
        cmd = get_cmd_with_device_params(device)

        cmd.extend(["evaluate", "\"%s\"" % EXPRESSION])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)

    def test_expression_with_symbol_load(self, device):
        """Tries using expression command with invalid C syntax"""

        if 'symbol' not in device.keys() or \
            'symbol_image' not in device.keys():
            pytest.skip("No symbol image path or symbol name")

        EXPRESSION = device['symbol']
        SYMBOL_FILE = device['symbol_image']

        cmd = get_cmd_with_device_params(device)

        cmd.extend(["evaluate", "\"%s\"" % EXPRESSION, "--symbols", "\"%s\"" % SYMBOL_FILE])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)
