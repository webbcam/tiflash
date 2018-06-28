/** 
 * verify.js - Verify include file that contains functions used
 * by main.js to verify images on devices.
 */


/**
 * Public function for handling verify commands
 
 * @param {server} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {args} verify arguments
 *
 * @returns {list} array of options
 */

function handle_verify_cmds(session, scriptEnv, args)
{
    var image = args.image.join(' ');

    if (!session.target.isConnected()) {
        session.target.connect();
    }

    if (args.binary) {
        return verify_binary(session, scriptEnv, image, args.address);
    } else {
        return verify_program(session, scriptEnv, image);
    }
}

/**
 * Verify function to verify image on flashed on device
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 */
function verify_program(session, scriptEnv, image)
{

    session.memory.verifyProgram(image);

    return true;
}

function verify_binary(session, scriptEnv, image, address)
{
    if (address == undefined) {
        address = 0x0000;
    }

    session.memory.verifyBinaryProram(image, Number(address));

    return true;
}


/**
 * Functions for setting verify options
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 */
/*
function set_verify_full_option(session, scriptEnv)
{
    _set_verify_option(session, scriptEnv, "Full verification");
}

function set_verify_fast_option(session, scriptEnv)
{
    _set_verify_option(session, scriptEnv, "Fast verification");
}

function set_verify_none_option(session, scriptEnv)
{
    _set_verify_option(session, scriptEnv, "No verification");
}
*/


/**
 * Core function for setting verify option,
 * called by wrapper functions
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {option} VerifyAfterProgramLoad option
 */
 /*
function _set_verify_option(session, scriptEnv, option)
{
    verify_id = "VerifyAfterProgramLoad";

    if (!session.flash.options.optionExist(verify_id)) {
        scriptEnv.tracewrite("Device does not support option for " + id);
    }

    try {
        session.flash.options.setString(verify_id, option); 
    } catch (e) {
        scriptEnv.tracewrite(e);
        return false;
    }

    return true;
}
*/
