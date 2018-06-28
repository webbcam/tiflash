/**
 * ccxml.js - include file that contains functions used
 * by main.js to generate ccxml files
 */

/**
 * Core function for generating ccxml file

 * @param {server} DSS Server object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {options} CCXML options
 */
function generate_ccxml(server, scriptEnv, options)
{
    var configGenerator = server.createTargetConfigurationGenerator();

    //  Set Config Directory
    configGenerator.setOutputDirectory(options.directory);
    //  Set Connection
    configGenerator.setConnection(options.connection.join(' '));
    //  Set Device
    configGenerator.setDevice(options.devicetype);
    //  Create Configuration
    configGenerator.createConfiguration(options.ccxml);

    /*
    try {
    //  Set Connection
        configGenerator.setConnection(options.connection.join(' '));
    //  Set Device
        configGenerator.setDevice(options.devicetype);
    //  Create Configuration
        configGenerator.createConfiguration(options.ccxml);
    } catch (e) {
        return false;
    }
    */

    return true;
}

/*
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

function print_connection_list(server, scriptEnv)
{
    var connections = get_connection_list(server, scriptEnv);
    for (var i in connections) {
        print(connections[i]);
    }
}

function print_device_list(server, scriptEnv)
{
    var devices = get_device_list(server, scriptEnv);
    for (var i in devices) {
        print(devices[i]);
    }
}
*/
