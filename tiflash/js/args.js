/** 
 * args.js - Arguments include file that handles reading and formatting
 * arguments from the command line (determines how main.js is called)
 */

function parse_args(args)
{
    args_obj = parse_cmds(args);
    for (var cmd in args_obj) {
        args_obj[cmd] = parse_options(args_obj[cmd]);
    }
    
    return args_obj;
}

function parse_cmds(args)
{
    return _create_args_obj(args, "--");
}

function parse_options(args)
{
    return _create_args_obj(args, "-");
}

function _create_args_obj(args, keyval)
{
    args_json = {};  //  any unknown args
    //args_json = {'positionals' : new Array()};
    current_key = 'positionals';
    
    for (var i = 0; i < args.length; i++) {
        //  keys start with --
        var arg = args[i];
        if (arg.slice(0, keyval.length) == keyval) {
            key = arg.slice(keyval.length);
            args_json[key] = new Array();
            current_key = key;
        } else {
            if (args_json.hasOwnProperty(current_key) == false) {
                args_json[current_key] = new Array();
            }
            args_json[current_key].push(arg);
        }
    }
    
    return args_json;
}
