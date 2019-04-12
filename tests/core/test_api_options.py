import pytest

import tiflash

class TestOptionsApi():

    # Getters
    def test_basic_get_option(self, tdev):
        """Tests basic get_option function"""
        result = tiflash.get_option(tdev['option'],
            serno=tdev['serno'],
            connection=tdev['connection'],
            devicetype=tdev['devicetype'])

        #assert result == 'true' or result == 'false'


    #TODO: add bool-option to test sets
    @pytest.mark.xfail
    def test_basic_get_bool_option(self, tdev):
        """Tests basic get_bool_option pass"""
        result = tiflash.get_bool_option(tdev['option'],
            serno=tdev['serno'],
            connection=tdev['connection'],
            devicetype=tdev['devicetype'])

        assert result == True or result == False

    @pytest.mark.xfail
    def test_basic_get_float_option(self, tdev):
        """Tests basic get_float_option function"""
        result = tiflash.get_float_option(tdev['option'],
            serno=tdev['serno'],
            connection=tdev['connection'],
            devicetype=tdev['devicetype'])

        assert type(result) == float

    @pytest.mark.skip
    def test_get_option_with_preop(self, tdev):
        """Tests get_option with a preop"""
        if 'ieee' not in tdev.keys():
            pytest.skip("No IEEE Address provided in setup.cfg for this device")

        result = tiflash.get_option("DeviceIeeePrimary",
            pre_operation="ReadPriIeee",
            serno=tdev['serno'],
            connection=tdev['connection'],
            devicetype=tdev['devicetype'])

        assert result == tdev['ieee']

    def test_get_invalid_option(self, tdev):
        """Tests get_option throws error when invalid option id provided"""
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.get_option("InvalidOption",
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

    def test_get_option_invalid_preop(self, tdev):
        """Tests get_option raises error when invalid preop provided"""
        with pytest.raises(tiflash.TIFlashError):
            result = tiflash.get_option("ResetOnRestart",
              pre_operation="InvalidOperation",
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])


    # Setters
    #@pytest.mark.xfail
    def test_basic_set_option(self, tdev):
        """Tests basic set_option function"""
        tiflash.set_option(
                option_id=tdev['option'],
                option_val="true",
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])


    # List
    def test_list_options(self, tdev):
        """Tests all options returned in list are valid"""
        options = tiflash.list_options(
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

        assert len(options) > 1

    def test_list_single_option(self, tdev):
        """Tests listing of one specified option"""
        option_to_test = tdev['option']

        options = tiflash.list_options(
                option_id=tdev['option'],
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

        assert len(options) == 1
        assert option_to_test in options.keys()

    def test_list_single_nonexistant_option(self, tdev):
        """Tests listing of specified option that does not exist"""
        options = tiflash.list_options(
                option_id="InvalidOption",
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

        assert len(options) == 0
