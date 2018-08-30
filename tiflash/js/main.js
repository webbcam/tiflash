/**
 * main.js - Main script that uses all other import scripts,
 * only script that should be called directly
 */
'use strict';

//importPackage(Packages.org.mozilla.javascript);


path = this.arguments[0];
port = parseInt(this.arguments[1]);
//print("PATH: " + this.arguments[0])
//print("PORT: " + this.arguments[1])
scriptEnv = null;
debugServer = null;
debugSession = null;
ccsServer = null;
ccsSession = null;

main();

function main()
{
    var retcode = 0;
    var result = "";

    //  Setup Scripting Environment
    scriptEnv = Packages.com.ti.ccstudio.scripting.environment.ScriptingEnvironment.instance();

    //  Set Directory relative to javascript files
    scriptEnv.setCurrentDirectory(path + "/js");


    load(scriptEnv.toAbsolutePath("args.js"));
    args = parse_args(this.arguments);


    //  Create Debug Server
    debugServer = scriptEnv.getServer('DebugServer.1');


    //  Set Trace Level
    if (args.debug) {
        scriptEnv.traceSetConsoleLevel(Packages.com.ti.ccstudio.scripting.environment.TraceLevel.ALL);
    } else {
        scriptEnv.traceSetConsoleLevel(Packages.com.ti.ccstudio.scripting.environment.TraceLevel.OFF);
    }


    //  Start Session
    if (args.session) {
        load(scriptEnv.toAbsolutePath("session.js"));

        try {
            debugSession = start_session(debugServer, scriptEnv, args.session);
        } catch (e) {
            result = e;
            retcode = -1;

            send_result(scriptEnv, port, result);
            quit(retcode);
        }

    }


    //  List commands
    if (args.list) {
        load(scriptEnv.toAbsolutePath("list.js"));
        try {
            result = handle_list_cmds(debugServer, scriptEnv, args.list);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }

    //  Print options
    if (args.printoptions) {
        load(scriptEnv.toAbsolutePath("options.js"));
        try {
            print_options(debugSession, scriptEnv, args.printoptions.id);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }



    //  Generate CCXML
    if (args.genccxml) {
        load(scriptEnv.toAbsolutePath("ccxml.js"));
        try {
            result = generate_ccxml(debugServer, scriptEnv, args.genccxml);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }


    //  Perform Operation
    if (args.operation) {
        load(scriptEnv.toAbsolutePath("operation.js"));

        try {
            handle_operation_cmds(debugSession, scriptEnv, args.operation);
        } catch (e) {
            result = e;
            retcode = -1;

            send_result(scriptEnv, port, result);
            quit(retcode);
        }
    }


    //  Set Option
    if (args.setoption) {
        load(scriptEnv.toAbsolutePath("options.js"));

        for (var id in args.setoption) {
            var val = args.setoption[id].join(' ');

            try {
                set_option(debugSession, scriptEnv, id, val);
            } catch (e) {
                result = e;
                retcode = -1;

                send_result(scriptEnv, port, result);
                quit(retcode);
            }
        }
    }


    //  Get Option
    if (args.getoption) {
        load(scriptEnv.toAbsolutePath("options.js"));

        var key = args.getoption.id.join(' ');

        try {
            result = get_option(debugSession, scriptEnv, key);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }


    //  Flash Device function
    if (args.flash) {
        load(scriptEnv.toAbsolutePath("flash.js"));

        try {
            handle_flash_cmds(debugSession, scriptEnv, args.flash);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }

    //  Standalone Erase function
    if (args.erase) {
        load(scriptEnv.toAbsolutePath("erase.js"));
        try {
            erase_entire_flash(debugSession, scriptEnv);
        } catch (e) {
            result = e;
            retcode = -1;
        }
        //send_result(scriptEnv, port, result);
        //quit(retcode);
    }

    //  Standalone Verify function
    if (args.verify) {
        load(scriptEnv.toAbsolutePath("verify.js"));
        try {
            handle_verify_cmds(debugSession, scriptEnv, args.verify);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }

    //  Board Reset function
    if (args.reset) {
        load(scriptEnv.toAbsolutePath("reset.js"));
        try {
            board_reset(debugSession, scriptEnv);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }

    //  Memory operations
    if (args.memory) {
        load(scriptEnv.toAbsolutePath("memory.js"));
        if (args.memory.read) {
            try {
                result = read_memory(debugSession, scriptEnv, args.memory.page,
                    args.memory.address, args.memory.numBytes);
            } catch (e) {
                result = e;
                retcode = -1;
            }
        } else if (args.memory.write) {
            try {
                result = write_memory(debugSession, scriptEnv,
                    args.memory.page, args.memory.address, args.memory.data)
            } catch (e) {
                result = e;
                retcode = -1;
            }
        }

        send_result(scriptEnv, port, result);
        quit(retcode);
    }

    //  Evaluate Function
    if (args.evaluate) {
        load(scriptEnv.toAbsolutePath("expression.js"));
        try {
            result = evaluate_expression(debugSession, scriptEnv, args.evaluate);
        } catch (e) {
            result = e;
            retcode = -1;
        }

        send_result(scriptEnv, port, result);
        quit(retcode);

    }


    send_result(scriptEnv, port, result);

    if (args.attach) {
        load(scriptEnv.toAbsolutePath("session.js"));

        attach_ccs(debugSession, scriptEnv, args.session);
    }

    quit(retcode);
}

function send_result(scriptEnv, port, result)
{
    load(scriptEnv.toAbsolutePath("result.js"));
    var result_str = String(result);

    //  Convert to ',' deliminated string
    if (result instanceof Array) {
        result_str = result.join(";;");
        //result_str = scriptEnv.arrayToString(result, ",");
    }


    //  Post Result to Python Socket
    return post_result(port, result_str);
}

function quit(retcode)
{

    if (debugSession)
	{
        //  Disconnect if connected
        if (debugSession.target.isConnected()) {
            debugSession.target.disconnect();
        }

        // Close debug session.
        debugSession.terminate();
    }

    if (debugServer)
	{
		debugServer.stop();
    }

    // Terminate JVM and return main return value.
    java.lang.System.exit(retcode);
}
