/**
 * memory.js - Memory include file that contains functions used
 * by main.js to write/read memory on devices.
 */

/**
 * Read Memory function to read bytes in device's memory

 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {page} page in memory to read from
 * @param {address} address in memory to begin reading
 * @param {numBytes} number of bytes to read
 */
function read_memory(session, scriptEnv, page, address, numBytes)
{
    if (!session.target.isConnected()) {
        session.target.connect();
    }

    return session.memory.readData(page, address, 8, numBytes);
}

/**
 * Write Memory function to write bytes to device's memory

 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {page} page in memory to write to
 * @param {address} address in memory to begin writing
 * @param {data} bytes to write
 */
function write_memory(session, scriptEnv, page, address, data)
{
    if (!session.target.isConnected()) {
        session.target.connect();
    }

    session.memory.writeData(page, address, 8, data);
    return true;
}
