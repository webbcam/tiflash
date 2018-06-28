/** 
 * flash.js - Flash include file that contains functions used
 * by main.js to flash devices.
 */
function handle_flash_cmds(session, scriptEnv, args)
{

    var image = args.image.join(' ');
    var retval = false;

    if (!session.target.isConnected()) {
        session.target.connect();
    }

    //  Flash Image(s)
    if (args.binary != undefined) {
        retval = load_binary(session, scriptEnv, image, args.address);
    //} else if (images.length == 1) {
    } else {
        retval = load_image(session, scriptEnv, image);
    }
    /*
    } else {
        //retval = load_multiple(session, scriptEnv, images);
        ;
    }
    */

    return retval;
}

function load_image(session, scriptEnv, image)
{
    session.memory.loadProgram(image);
    return true;
}


function load_binary(session, scriptEnv, image, address)
{
    if (address == undefined) {
        address = 0x0000;
    }

    session.memory.loadBinaryProgram(image, Number(address));
    return true;
}


function load_multiple(session, scriptEnv, images)
{
    var ret = false;
    //  Need to disable reset after load for multiload (will hang otherwise)
    session.options.setBoolean("AutoRunToLabelOnRestart", false);
    session.options.setBoolean("ResetOnRestart", false);
    session.flash.multiloadStart();
    for (var i = 0; i < images.length; i++) {
        ret = load_image(session, scriptEnv, images[i]);
        if (ret == false) {
            break;
        }
    }
    session.flash.multiloadEnd();
    return ret;
}

/*
function set_option(session, scriptEnv, option_id, option_val)
{
    if (!session.options.optionExist(option_id)) {
        scriptEnv.tracewrite("Device does not support option for " + id);
        return false;
    }

    var type = session.options.getValueType(option_id);

    try {
        if (type == "string")
            session.flash.options.setString(option_id, option_val); 
        else if (type == "boolean")
            session.flash.options.setBoolean(option_id, option_val == "true");
        else if (type == "numeric")
            session.flash.options.setNumeric(option_id, Number(option_val));
        else
            return false;


    } catch (e) {
        scriptEnv.tracewrite(e);
        return false;
    }

    return true;

}

function get_option(session, scriptEnv, option_id)
{
    if (!session.options.optionExist(option_id)) {
        scriptEnv.tracewrite("Device does not support option for " + id);
        return false;
    }

    var type = session.options.getValueType(option_id);
    var val = null;

    try {
        if (type == "string")
            val = session.flash.options.getString(option_id); 
        else if (type == "boolean")
            val = session.flash.options.getBoolean(option_id);
        else if (type == "numeric")
            val = session.flash.options.getNumeric(option_id);
        else
            return null;


    } catch (e) {
        scriptEnv.tracewrite(e);
        return null;
    }

    return val;

}
*/
