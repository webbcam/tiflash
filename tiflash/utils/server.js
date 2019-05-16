/*
 *  server.js - Runs a DebugServer process
 */

'use strict';

load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/utils/json2.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/DebugServer.js");
load(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/handlers.js");

package_info = JSON.parse(readFile(java.lang.System.getenv("DSS_SCRIPTING_ROOT") + "/package.json"));

/* print("--- " + package_info.name + " (" + package_info.version + ")" + " ---"); */

config = {
    "cwd": "/path/to/repo/debugserver-js",   /* Currently not necessary */
    "debug": false

};

var port = 0; // By default if no port is provided, will use Java's automatic port allocation

/* First arg should be the port number to use for the Debug Server */
if (this.arguments.length > 0) {
    port = parseInt(this.arguments[0]);
}

var socket = ServerSocket(port);
port = socket.getLocalPort();

var server = new DebugServer(config, socket);
server.addSessionHandlers(sessionHandlers);

print("PORT: " + port);

server.run();
server.shutdown();

java.lang.System.exit(0);
