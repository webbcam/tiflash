import pytest
import subprocess

from clihelpers import get_cmd_with_device_params

class TestExpressionCli():

    def test_basic_expression(self, tdev):
        """Runs a simple gel command"""
        EXPRESSION = tdev['expression-name']

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["evaluate", "\"%s\"" % EXPRESSION])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)

    def test_invalid_expression_format(self, tdev):
        """Tries using expression command with invalid C syntax"""

        EXPRESSION = "var i = 0"
        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["evaluate", "\"%s\"" % EXPRESSION])
        cmd_str = " ".join(cmd)

        with pytest.raises(subprocess.CalledProcessError):
            subprocess.check_call(cmd_str, shell=True)

    def test_expression_with_symbol_load(self, tdev):
        """Tries using expression command with invalid C syntax"""

        if 'symbol-name' not in tdev.keys() or \
            'symbol-image' not in tdev.keys():
            pytest.skip("No symbol image path or symbol name")

        EXPRESSION = tdev['symbol-name']
        SYMBOL_FILE = tdev['symbol-image']

        cmd = get_cmd_with_device_params(tdev)

        cmd.extend(["evaluate", "\"%s\"" % EXPRESSION, "--symbols", "\"%s\"" % SYMBOL_FILE])
        cmd_str = " ".join(cmd)

        subprocess.check_call(cmd_str, shell=True)
