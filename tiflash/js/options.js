/** 
 * options.js - Options include file that handles both setoption and getoption
 * commands
 */

/**
 * Public function for handling list options
 
 * @param {server} DSS Server object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {options} list options
 *
 * @returns {list} array of options
 */

function set_option(session, scriptEnv, option_id, option_val)
{
    if (!session.options.optionExist(option_id)) {
        throw("Device does not support option for " + id);
    }

    var type = session.options.getValueType(option_id);

    if (type == "string")
        session.flash.options.setString(option_id, option_val); 
    else if (type == "boolean")
        session.flash.options.setBoolean(option_id, option_val == "True");
    else if (type == "numeric")
        session.flash.options.setNumeric(option_id, Number(option_val));
    else
        return false;

    return true;

}

function get_option(session, scriptEnv, option_id)
{
    if (!session.options.optionExist(option_id)) {
        throw("Device does not support option for " + id);
    }

    var type = session.options.getValueType(option_id);
    var val = null;

    if (type == "string")
        val = session.flash.options.getString(option_id); 
    else if (type == "boolean")
        val = session.flash.options.getBoolean(option_id);
    else if (type == "numeric")
        val = session.flash.options.getNumeric(option_id);
    else
        val = null;


    return val;

}

function print_options(session, scriptEnv, option_id)
{
    print("OPTIONS:");
    if (!option_id) {
        option_id = ".*";
    }


    //  Turn on output just for this command
    scriptEnv.traceSetConsoleLevel(Packages.com.ti.ccstudio.scripting.environment.TraceLevel.ALL);

    session.flash.options.printOptions(option_id);
    session.flash.listSupportedOperations();

    //  Turn off output upon finishing
    scriptEnv.traceSetConsoleLevel(Packages.com.ti.ccstudio.scripting.environment.TraceLevel.OFF);
}
