/** 
 * operation.js - Operations include file that handles device 
 * flash operations commands
 */

/**
 * Public function for handling operation cmds
 
 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {args} operation arguments
 *
 * @returns {retval} return status (boolean)
 */
function handle_operation_cmds(session, scriptEnv, args)
{
    var retval = false;
    //  Check if flash is usable
    if (session.flash.isFlashSupported() != true) {
        throw "Flash is not supported on this device.";
    } else {
        //  Check if device is connected
        if (session.target.isConnected() == false) {
            session.target.connect();
        }

        session.flash.performOperation(args.opcode);
        retval = true;
    }

    return retval;
}
