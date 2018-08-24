/**
 * session.js - Session include file that handles functionality of
 * Debug Server Session commands
 */

importPackage(Packages.java.lang)

/**
 * Public function for handling session commands

 * @param {server} DSS Server object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {args} sesion arguments
 *
 * @returns {session} Debug Server Session
 */
function start_session(server, scriptEnv, args)
{
    //  TODO: add check for args.session.ccxml
    server.setConfig(args.ccxml);

    //  TODO: add check for args.session.chip
    var debugSession = server.openSession(".*" + args.chip + ".*");

    //  Set Session Timeout
    debugSession.setScriptTimeout(Number(args.timeout));


    //  Connect to board
    debugSession.target.connect();
    /*
    //  Connect only if specified
    if (args.connect) {
        debugSession.target.connect();
    }
    */

    return debugSession;
}

/**
 * Public function for attaching CCS to Debug Server Session

 * @param {session} DSS Session object for device.
 * @param {scriptEnv} DSS Scripting Environment object.
 * @param {args} session arguments
 *
 * @returns {session} Debug Server Session
 */
function attach_ccs(session, scriptEnv, args)
{
    scriptEnv.traceSetConsoleLevel(Packages.com.ti.ccstudio.scripting.environment.TraceLevel.OFF);

    var ccsServer = scriptEnv.getServer('CCSServer.1');
    var ccsSession = ccsServer.openSession(session.getName());

    var stdin = new BufferedReader( new InputStreamReader(System['in']) );
    while (!stdin.ready()) {
        java.lang.Thread.sleep(500);
    }

    ccsSession.terminate();
    ccsServer.stop();
}
