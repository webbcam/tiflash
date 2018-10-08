import argparse


def get_session_args(args):
    """Pulls session args from 'args' and returns a dictionary for passing to
    functions.

    Args:
        args (argparse.namespace): args parsed by argparser

    Returns:
        dict: dictionary of session specific arguments (taken from 'args')
    """
    session_args = dict()

    if args.ccs:
        session_args['ccs'] = args.ccs
    if args.ccxml:
        session_args['ccxml'] = args.ccxml
    if args.timeout:
        session_args['timeout'] = args.timeout
    if args.devicetype:
        session_args['devicetype'] = args.devicetype
    if args.connection:
        session_args['connection'] = args.connection
    if args.serno:
        session_args['serno'] = args.serno
    if args.chip:
        session_args['chip'] = args.chip
    if args.debug:
        session_args['debug'] = args.debug
    if args.fresh:
        session_args['fresh'] = args.fresh
    if args.attach:
        session_args['attach'] = args.attach

    return session_args

def set_subparser_arg_titles(parser, positionals=None, optionals=None):
    parser._positionals.title = positionals or "Command Arguments"
    parser._optionals.title = optionals or "Command Arguments"


# Session Parser - standard args for creating DSS Session
SessionParser = argparse.ArgumentParser(prog="tiflash", add_help=False)
SessionParser.add_argument('-s', '--serno', help='Serial number of device')
SessionParser.add_argument('-d', '--devicetype', help='Devicetype of device')
SessionParser.add_argument('--ccs', type=int, default=None,
                           help='Version (int) of ccs to use (default=latest)')
SessionParser.add_argument('--ccxml', help='CCXML (full path) file to use')
SessionParser.add_argument('--connection', default=None,
                           help='Connection type to use for device')
SessionParser.add_argument('--chip', help='Device core to use')
SessionParser.add_argument('-t', '--timeout', default=None, type=float,
                           help='Timeout to use for command (seconds)')
SessionParser.add_argument('-F', '--fresh', action='store_true',
                           help='Generate new (fresh) ccxml')
SessionParser.add_argument('-D', '--debug', action='store_true',
                           help='Display debugging output')
SessionParser.add_argument('-A', '--attach', action='store_true',
                           help='Attach CCS to Device after performing action')


# Option Parser - used for getting/setting options
OptionsGetParser = argparse.ArgumentParser(add_help=False)
OptionsGetParser.add_argument('optionID', metavar='optionID',
                           help="Option ID to get value of.")
OptionsGetParser.add_argument('-op', '--operation', metavar='preOperation',
                           help='''Specify an operation to perform prior to
                            getting/setting option''')

OptionsListParser = argparse.ArgumentParser(add_help=False)
OptionsListParser.add_argument('optionID', metavar='optionID', nargs='?',
                           help="Option ID to get info on.")

# List Parser
ListParser = argparse.ArgumentParser(add_help=False)
ListParser.add_argument('--devicetypes', action='store_true',
                        help='Prints list of installed devicetypes')
ListParser.add_argument('--connections', action='store_true',
                        help='Prints list of installed connections')
ListParser.add_argument('--cpus', action='store_true',
                        help='Prints list of installed cpus')
#ListParser.add_argument('--cfgs', action='store_true',
#                        help='Prints list of installed target cfgs')
ListParser.add_argument('--options', action='store_true',
                        help='Prints list of target options')
ListParser.add_argument('-f', '--filter', metavar='filter', dest='search',
                        type=str, help='String to filter results by')


# Reset Parser
ResetParser = argparse.ArgumentParser(add_help=False)
ResetParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar='optionID optionValue',
                         help='Sets an option before running reset cmd')


# Erase Parser
EraseParser = argparse.ArgumentParser(add_help=False)
EraseParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar='optionID optionValue',
                         help='Sets an option before running erase cmd')


# Verify Parser
VerifyParser = argparse.ArgumentParser(add_help=False)
VerifyParser.add_argument('image', metavar='image', nargs=1, help='''Image to verify.''')
VerifyParser.add_argument('-b', '--bin', action='store_true',
                         help='Specify if image is a binary image')
#VerifyParser.add_argument('-i', '--image', action='append', metavar='image',
#                          help='Image to verify can repeat -i/--image command')
VerifyParser.add_argument('-o', '--option', nargs=2, action='append',
                          dest='options', metavar='optionID optionValue',
                          help='Sets an option before running verify cmd')


# Flash Parser
FlashParser = argparse.ArgumentParser(add_help=False)
FlashParser.add_argument('images', metavar='image', nargs=1, help='''Image to flash.''')
FlashParser.add_argument('-b', '--bin', action='store_true',
                         help='Specify if image(s) are binary images')
FlashParser.add_argument('-a', '--address', metavar='address',
                         help='Address to begin flashing image(s)')
FlashParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar=('optionID', 'optionValue'),
                         help='sets an option before running flash cmd')

# Memory Read Parser
MemoryReadParser = argparse.ArgumentParser(add_help=False)
MemoryReadParser.add_argument('address', help="Address in memory to read from")
MemoryReadParser.add_argument('-p', '--page', default=0,
                            help="Page number in memory to access address")
MemoryReadParser.add_argument('-n', '--num', dest='num_bytes', default=1,
                            help="Number of bytes to read")
MemoryReadParser.add_argument('--hex', action='store_true',
                            help="Displays output in hex")

# Memory Write Parser
MemoryWriteParser = argparse.ArgumentParser(add_help=False)
MemoryWriteParser.add_argument('address', help="Address in memory to write to")
MemoryWriteParser.add_argument('-p', '--page', default=0,
                            help="Page number in memory to access address")
MemoryWriteParser.add_argument('-d', '--data', nargs='+', required=True,
                            help="""Bytes (hex) to write to memory.
                            Each byte separated by a space""")

# Register Read Parser
RegisterReadParser = argparse.ArgumentParser(add_help=False)
RegisterReadParser.add_argument('regname', help="Name of register to read.")
RegisterReadParser.add_argument('--hex', action='store_true',
                            help="Displays output in hex")

# Register Write Parser
RegisterWriteParser = argparse.ArgumentParser(add_help=False)
RegisterWriteParser.add_argument('regname', help="Name of register to read.")
RegisterWriteParser.add_argument('value',
                            help="Value (32bit hex) to write to register.")

# Expression Parser
ExpressionParser = argparse.ArgumentParser(add_help=False)
ExpressionParser.add_argument('expression',
                            help="C or GEL expression to execute")
ExpressionParser.add_argument('--symbols', required=False, default=None,
                            help=""".out or GEL symbol file to load before
                            evaluating expression.""")

# Attach Parser
AttachParser = argparse.ArgumentParser(add_help=False)

# XDS110Reset Parser
XDS110ResetParser = argparse.ArgumentParser(add_help=False)

# XDS110Upgrade Parser
XDS110UpgradeParser = argparse.ArgumentParser(add_help=False)

# XDS110List Parser
XDS110ListParser = argparse.ArgumentParser(add_help=False)

# Detect Parser
DetectParser = argparse.ArgumentParser(add_help=False)
