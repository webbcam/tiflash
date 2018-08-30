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


# Session Parser - standard args for creating DSS Session
SessionParser = argparse.ArgumentParser(prog="TIFlash", add_help=False)
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
OptionsParser = argparse.ArgumentParser(add_help=False)
OptionsParser.add_argument('--get', metavar='optionID',
                           help='Gets value of given option id')
OptionsParser.add_argument('--set', nargs=2, metavar='optionID optionValue',
                           help='Sets optionID to optionValue')
OptionsParser.add_argument('-op', '--operation', metavar='preOperation',
                           help='''Specify an operation to perform prior to
                            getting/setting option''')
OptionsParser.add_argument('-l', '--list', metavar='optionID', dest='optionID',
                           default=None, nargs='?',
                           help='''List information on all or one
                            particular option''')

# List Parser
ListParser = argparse.ArgumentParser(add_help=False)
ListParser.add_argument('-d', '--devices', action='store_true',
                        help='Prints list of installed devices')
ListParser.add_argument('-c', '--connections', action='store_true',
                        help='Prints list of installed connections')
ListParser.add_argument('-u', '--cpus', action='store_true',
                        help='Prints list of installed cpus')
ListParser.add_argument('-cfg', '--cfgs', action='store_true',
                        help='Prints list of installed target cfgs')
ListParser.add_argument('-o', '--options', action='store_true',
                        help='Prints list of target options')


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
VerifyParser.add_argument('-i', '--image', action='append', metavar='image',
                          help='Image to verify can repeat -i/--image command')
VerifyParser.add_argument('-o', '--option', nargs=2, action='append',
                          dest='options', metavar='optionID optionValue',
                          help='Sets an option before running verify cmd')


# Flash Parser
FlashParser = argparse.ArgumentParser(add_help=False)
FlashParser.add_argument('images', metavar='image1 [image2, ...]', nargs='+',
                         help='''Image(s) to flash. any images specified by '-i'
                        option are appended to the image list provided here''')
FlashParser.add_argument('-i', '--image', dest='images',
                         required=False, action='append', metavar='image',
                         help='Image to flash can repeat -i/--image command')
FlashParser.add_argument('-b', '--bin', action='store_true',
                         help='Specify if image(s) are binary images')
FlashParser.add_argument('-a', '--address', metavar='address',
                         help='Address to begin flashing image(s)')
FlashParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar=('optionID', 'optionValue'),
                         help='sets an option before running flash cmd')

# Memory Parser
MemoryParser = argparse.ArgumentParser(add_help=False)
MemoryParser.add_argument('-r', '--read', action='store_true',
                            help="Read bytes from device memory")
MemoryParser.add_argument('-w', '--write', action='store_true',
                            help="Write bytes to device memory")
MemoryParser.add_argument('-a', '--address', required=True,
                            help="Address in memory to read/write from/to")
MemoryParser.add_argument('-d', '--data', nargs='+',
                            help="Space separated list of bytes (in hex) to \
                            write (WRITE ONLY)")
MemoryParser.add_argument('-n', '--num', dest='num_bytes', default=1,
                            help="Number of bytes to read (READ ONLY)")
MemoryParser.add_argument('-p', '--page', default=0,
                            help="Page number in memory to access address")
MemoryParser.add_argument('-H', '--hex', action='store_true',
                            help="Displays output in hex (READ ONLY)")

# Expression Parser
ExpressionParser = argparse.ArgumentParser(add_help=False)
ExpressionParser.add_argument('expression', help="C or GEL expression to execute")
ExpressionParser.add_argument('--symbols', required=False, default=None,
                            help=""".out or GEL symbol file to load before
                            evaluating expression.""")

# Attach Parser
AttachParser = argparse.ArgumentParser(add_help=False)
