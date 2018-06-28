/** 
 * erase.js - Erase include file that contains functions used
 * by main.js to erase devices.
 */

ERASE_OPTIONS = 
    {   "all" : "All Unprotected Sectors",
        "necessary" : "Necessary Sectors Only",
        "retain" : 
            "Necessary Sectors Only (Retain untouched content within sector)",
        "none" : "Program Load Only (do not erase sectors)"
    };

/**
 * Erase function to erase device's entire flash
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 */
function erase_entire_flash(session, scriptEnv)
{
    //  Allow exception to be thrown - calling script should catch

    if (session.target.isConnected()) {
        session.target.connect();
    }

    session.flash.erase();

    return true;
}

/**
 * Functions for setting erase options
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 */
/*
function set_erase_all_option(session, scriptEnv)
{
    _set_erase_option(session, scriptEnv, "All Unprotected Sectors");
}

function set_erase_necessary_option(session, scriptEnv)
{
    _set_erase_option(session, scriptEnv, "Necessary Sectors Only");
}

function set_erase_retain_option(session, scriptEnv)
{
    _set_erase_option(session, scriptEnv, "Necessary Sectors Only (Retain untouched content within sector)");
}

function set_erase_none_option(session, scriptEnv)
{
    _set_erase_option(session, scriptEnv, "Program Load Only (do not erase sectors)");
}
*/

/**
 * Core function for setting erase option, to be 
 * called by wrapper functions
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {options} FlashEraseSettings option (erase_options object keys).
 */
/*
function _set_erase_option(session, scriptEnv, option)
{
    erase_id = "FlashEraseSetting";

    if (!session.flash.options.optionExist(erase_id)) {
        scriptEnv.tracewrite("Device does not support option for " + id);
    }

    try {
        session.flash.options.setString(erase_id, option); 
    } catch (e) {
        scriptEnv.tracewrite(e);
        return false;
    }

    return true;
}
*/
