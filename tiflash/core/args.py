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

    return session_args


# Session Parser - standard args for creating DSS Session
SessionParser = argparse.ArgumentParser(prog="TIFlash", add_help=False)
SessionParser.add_argument('-s', '--serno', help='serial number of device')
SessionParser.add_argument('-d', '--devicetype', help='devicetype of device')
SessionParser.add_argument('--ccs', type=int, default=None,
                           help='version (int) of ccs to use (default=latest)')
SessionParser.add_argument('--ccxml', help='ccxml (full path) file to use')
SessionParser.add_argument('--connection', default=None,
                           help='connection type to use for device')
SessionParser.add_argument('--chip', help='core to use')
SessionParser.add_argument('-F', '--fresh', action='store_true',
                           help='generate new (fresh) ccxml')
SessionParser.add_argument('-D', '--debug', action='store_true',
                           help='display debugging output')


# Option Parser - used for getting/setting options
OptionsParser = argparse.ArgumentParser(add_help=False)
OptionsParser.add_argument('--get', metavar='optionID',
                           help='gets value of given option id')
OptionsParser.add_argument('--set', nargs=2, metavar='optionID optionValue',
                           help='sets optionID to optionValue')
OptionsParser.add_argument('-op', '--operation', metavar='preOperation',
                           help='''specify an operation to perform prior to
                            getting/setting option''')
OptionsParser.add_argument('-l', '--list', metavar='optionID', dest='optionID',
                           default=None, nargs='?',
                           help='''list information on all or one
                            particular option''')

# List Parser
ListParser = argparse.ArgumentParser(add_help=False)
ListParser.add_argument('-d', '--devices', action='store_true',
                        help='prints list of installed devices')
ListParser.add_argument('-c', '--connections', action='store_true',
                        help='prints list of installed connections')
ListParser.add_argument('-u', '--cpus', action='store_true',
                        help='prints list of installed cpus')
ListParser.add_argument('-cfg', '--cfgs', action='store_true',
                        help='prints list of installed target cfgs')
ListParser.add_argument('-o', '--options', action='store_true',
                        help='prints list of target options')


# Reset Parser
ResetParser = argparse.ArgumentParser(add_help=False)
ResetParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar='optionID optionValue',
                         help='sets an option before running reset cmd')


# Erase Parser
EraseParser = argparse.ArgumentParser(add_help=False)
EraseParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar='optionID optionValue',
                         help='sets an option before running erase cmd')


# Verify Parser
VerifyParser = argparse.ArgumentParser(add_help=False)
VerifyParser.add_argument('-i', '--image', action='append', metavar='image',
                          help='image to verify can repeat -i/--image command')
VerifyParser.add_argument('-o', '--option', nargs=2, action='append',
                          dest='options', metavar='optionID optionValue',
                          help='sets an option before running verify cmd')


# Flash Parser
FlashParser = argparse.ArgumentParser(add_help=False)
FlashParser.add_argument('images', metavar='image1 [image2, ...]', nargs='+',
                         help='''image(s) to flash. any images specified by '-i'
                        option are appended to the image list provided here''')
FlashParser.add_argument('-i', '--image', dest='images',
                         required=False, action='append', metavar='image',
                         help='image to flash can repeat -i/--image command')
FlashParser.add_argument('-b', '--bin', action='store_true',
                         help='specify if image(s) are binary images')
FlashParser.add_argument('-a', '--address', metavar='address',
                         help='address to begin flashing image(s)')
FlashParser.add_argument('-o', '--option', nargs=2, action='append',
                         dest='options', metavar=('optionID', 'optionValue'),
                         help='sets an option before running flash cmd')
