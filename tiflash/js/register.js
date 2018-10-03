/**
 * register.js - register include file that contains functions used
 * by main.js to write/read to a register on devices.
 */

/**
 * Read register function to read register value of a device

 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {regname} register name to read value of
 */
function read_register(session, scriptEnv, regname)
{
    if (!session.target.isConnected()) {
        session.target.connect();
    }

    return session.memory.readRegister(regname);
}

/**
 * Write register function to write value to device's register

 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {regname} register name to read value of
 * @param {value} value to write to register
 */
function write_register(session, scriptEnv, regname, value)
{
    if (!session.target.isConnected()) {
        session.target.connect();
    }

    session.memory.writeRegister(regname, value);
    return true;
}
