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

        if 'option-val' in tdev.keys():
            assert result == tdev['option-val']

    def test_get_option_with_preop(self, tdev):
        """Tests get_option with a preop"""
        if 'preop' not in tdev.keys():
            pytest.skip("No preop provided for device")

        result = tiflash.get_option(tdev['preop-option'],
            pre_operation=tdev['preop'],
            serno=tdev['serno'],
            connection=tdev['connection'],
            devicetype=tdev['devicetype'])


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
            result = tiflash.get_option(tdev['preop-option'],
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
                option_val=tdev['option-val'],
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])


    # List
    @pytest.mark.skip("List Options not implemented yet.")
    def test_list_options(self, tdev):
        """Tests all options returned in list are valid"""
        options = tiflash.list_options(
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

        assert len(options) > 1

    @pytest.mark.skip("List Options not implemented yet.")
    def test_list_single_option(self, tdev):
        """Tests listing of one specified option"""
        options = tiflash.list_options(
                option_id=tdev['option'],
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

        assert len(options) == 1
        assert tdev['option'] in options.keys()

    @pytest.mark.skip("List Options not implemented yet.")
    def test_list_single_nonexistant_option(self, tdev):
        """Tests listing of specified option that does not exist"""
        options = tiflash.list_options(
                option_id="InvalidOption",
                serno=tdev['serno'],
                connection=tdev['connection'],
                devicetype=tdev['devicetype'])

        assert len(options) == 0
