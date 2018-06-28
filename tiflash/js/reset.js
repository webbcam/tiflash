/** 
 * reset.js - Reset include file that contains functions used
 * by main.js to reset devices.
 */

/**
 * Reset function to board reset device
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 */
function board_reset(session, scriptEnv)
{
    session.target.reset();

    return true;
}

/**
 * Functions for setting reset after flash
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 */
function set_reset_after_flash(session, scriptEnv)
{
    _set_reset_after_flash(session, scriptEnv, true);
}

function unset_reset_after_flash(session, scriptEnv)
{
    _set_reset_after_flash(session, scriptEnv, false);
}

/**
 * Core function for setting reset after flash option,
 * called by wrapper functions
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {value} ResetOnRestart boolean value
 */
function _set_reset_after_flash(session, scriptEnv, value)
{
    reset_id = "ResetOnRestart";

    if (!session.flash.options.optionExist(reset_id)) {
        scriptEnv.tracewrite("Device does not support option for " + id);
    }

    try {
        session.options.setBoolean(reset_id, value);
    } catch (e) {
        scriptEnv.tracewrite(e);
        return false;
    }

    return true;
}

