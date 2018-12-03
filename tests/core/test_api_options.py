import pytest

import tiflash

@pytest.mark.usefixtures("device")
class TestOptionsApi():

    # Getters
    def test_basic_get_option(self, device):
        """Tests basic get_option function"""
        result = tiflash.get_option("ResetOnRestart",
            serno=device['serno'],
            connection=device['connection'],
            devicetype=device['devicetype'])

        assert result == 'true' or result == 'false'


    @pytest.mark.xfail
    def test_basic_get_bool_option(self, device):
        """Tests basic get_bool_option pass"""
        result = tiflash.get_bool_option("ResetOnRestart",
            serno=device['serno'],
            connection=device['connection'],
            devicetype=device['devicetype'])

        assert result == True or result == False

    @pytest.mark.xfail
    def test_basic_get_float_option(self, device):
        """Tests basic get_float_option function"""
        result = tiflash.get_float_option("DeviceInfoRevision",
            serno=device['serno'],
            connection=device['connection'],
            devicetype=device['devicetype'])

        assert type(result) == float

    def test_get_option_with_preop(self, device):
        """Tests get_option with a preop"""
        if 'ieee' not in device.keys():
            pytest.skip("No IEEE Address provided in setup.cfg for this device")

        result = tiflash.get_option("DeviceIeeePrimary",
            pre_operation="ReadPriIeee",
            serno=device['serno'],
            connection=device['connection'],
            devicetype=device['devicetype'])

        assert result == device['ieee']

    def test_get_invalid_option(self, device):
        """Tests get_option throws error when invalid option id provided"""
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.get_option("InvalidOption",
                serno=device['serno'],
                connection=device['connection'],
                devicetype=device['devicetype'])

    def test_get_option_invalid_preop(self, device):
        """Tests get_option raises error when invalid preop provided"""
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.get_option("ResetOnRestart",
              pre_operation="InvalidOperation",
                serno=device['serno'],
                connection=device['connection'],
                devicetype=device['devicetype'])


    # Setters
    @pytest.mark.xfail
    def test_basic_set_option(self, device):
        """Tests basic set_option function"""
        tiflash.set_option(option_id="ResetOnRestart", value="true")


    # List
    def test_list_options(self, device):
        """Tests all options returned in list are valid"""
        options = tiflash.list_options(
                serno=device['serno'],
                connection=device['connection'],
                devicetype=device['devicetype'])

        assert len(options) > 1

#   Takes way too long
#        for option in options.keys():
#            result = tiflash.get_option(option,
#                serno=device['serno'],
#                connection=device['connection'],
#                devicetype=device['devicetype'])

    def test_list_single_option(self, device):
        """Tests listing of one specified option"""
        option_to_test = "DeviceInfoRevision"

        options = tiflash.list_options(
                option_id=option_to_test,
                serno=device['serno'],
                connection=device['connection'],
                devicetype=device['devicetype'])

        assert len(options) == 1
        assert option_to_test in options.keys()

    def test_list_single_nonexistant_option(self, device):
        """Tests listing of specified option that does not exist"""
        options = tiflash.list_options(
                option_id="InvalidOption",
                serno=device['serno'],
                connection=device['connection'],
                devicetype=device['devicetype'])

        assert len(options) == 0
