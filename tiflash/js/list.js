/** 
 * list.js - List include file that handles any 'list' commands
 */

/**
 * Public function for handling list options
 
 * @param {server} DSS Server object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {options} list options
 *
 * @returns {list} array of options
 */
function handle_list_cmds(server, scriptEnv, options)
{
    var list = [];
    // CPUs 
    if (options.cpus) {
        var cpus = server.getListOfCPUs();

        list = cpus;

    //  Connections
    } else if (options.connections) {
        //load(scriptEnv.toAbsolutePath("ccxml.js"));
        var connections = get_connection_list(debugServer, scriptEnv);

        list = connections;
    
    //  Devices
    } else if (options.devices) {
        //load(scriptEnv.toAbsolutePath("ccxml.js"));
        var devices = get_device_list(debugServer, scriptEnv);

        list = devices;
    }

    return list;
}

function get_connection_list(server, scriptEnv)
{
    var configGenerator = server.createTargetConfigurationGenerator();

    return configGenerator.getListOfConnections();
}

function get_device_list(server, scriptEnv)
{
    var configGenerator = server.createTargetConfigurationGenerator();

    return configGenerator.getListOfDevices();
}

function get_configuration_list(server, scriptEnv)
{
    var configGenerator = server.createTargetConfigurationGenerator();

    return configGenerator.getListOfConfigurations();
}
