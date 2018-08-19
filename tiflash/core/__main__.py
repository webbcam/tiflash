import argparse
from platform import python_version
from pprint import pprint

from tiflash import core, __version__
from tiflash.core.args import (
    SessionParser,
    OptionsParser,
    ListParser,
    ResetParser,
    EraseParser,
    VerifyParser,
    FlashParser,
    MemoryParser,
    ExpressionParser,

    get_session_args
)

def generate_parser():
    """Generates an argument parser

    Returns:
        argparse.ArgumentParser
    """
    version = "tiflash: %s - python: %s" % (__version__, python_version())

    main_parser = argparse.ArgumentParser(prog="TIFlash",
                                          parents=[SessionParser])
    main_parser.add_argument('-v', '--version', action='version',
                        version=__version__,
                        help='print tiflash version')
    main_parser.add_argument('-V', '--VERSION', action='version',
                        version=version,
                        help='print tiflash & python version')

    sub_parsers = main_parser.add_subparsers(dest='cmd')
    sub_parsers.add_parser('option', parents=[OptionsParser],
        description="Get or set a device option.")
    sub_parsers.add_parser('list', parents=[ListParser],
        description="List device/environment information.")
    sub_parsers.add_parser('reset', parents=[ResetParser],
        description="Reset a device. (Board Reset)")
    sub_parsers.add_parser('erase', parents=[EraseParser],
        description="Erase a device's flash.")
    sub_parsers.add_parser('verify', parents=[VerifyParser],
        description="Verify an image on a device's flash.")
    sub_parsers.add_parser('flash', parents=[FlashParser],
        description="Flash a device with an image(s).")
    sub_parsers.add_parser('memory', parents=[MemoryParser],
        description="Read/Write memory location on a device.")
    sub_parsers.add_parser('evaluate', parents=[ExpressionParser],
        description="Evaluate a C/GEL expression on a device.")


    return main_parser


def parse_args():
    """Parses input parameters and displays help message.

    Returns:
        argparse.Namespace: provided arguments

    """
    # Generate parser
    main_parser = generate_parser()

    # Parser arguments
    args = main_parser.parse_args()

    return args


def handle_option(args):
    """Helper function for handling 'option' command"""
    session_args = get_session_args(args)
    # Get Option
    if args.get:
        try:
            value = core.get_option(args.get, pre_operation=args.operation,
                                   **session_args)
            print(value)
        except Exception as e:
            print(e)

    # Set Option
    elif args.set:
        print("Setting Option is unsupported at this time")
        pass

    # Display Option Information
    else:
        # TODO: Make this prettier
        # core.print_options(option_id=args.info, **session_args)
        options = core.list_options(option_id=args.optionID, **session_args)
        print("Options (%s):" % args.optionID if args.optionID else "Options:")
        pprint(options)  # lazy


def handle_list(args):
    """Helper function for handling 'list' command"""
    results = []
    session_args = get_session_args(args)
    if args.devices:
        results = core.get_devices(args.ccs)
    elif args.connections:
        results = core.get_connections(args.ccs)
    elif args.cpus:
        results = core.get_cpus(args.ccs)
    elif args.options:
        # core.print_options(**session_args)
        results = core.list_options(**session_args)

    for e in results:
        print(e)


def handle_reset(args):
    """Helper function for handling 'reset' command"""
    session_args = get_session_args(args)
    options = dict()

    if args.options:
        for opt in args.options:
            option_id = opt[0]
            option_value = opt[1]

            options.update({option_id: option_value})

    if len(options) == 0:
        options = None

    try:
        result = core.reset(options=options, **session_args)
        print(result)
    except Exception as e:
        print(e)


def handle_erase(args):
    """Helper function for handling 'erase' command"""
    session_args = get_session_args(args)
    options = dict()

    if args.options:
        for opt in args.options:
            option_id = opt[0]
            option_value = opt[1]

            options.update({option_id: option_value})

    if len(options) == 0:
        options = None

    try:
        result = core.erase(options=options, **session_args)
        print(result)
    except Exception as e:
        print(e)


def handle_verify(args):
    """Helper function for handling 'verify' command"""
    session_args = get_session_args(args)
    options = dict()

    if args.options:
        for opt in args.options:
            option_id = opt[0]
            option_value = opt[1]

        options.update({option_id: option_value})

    if len(options) == 0:
        options = None

    # TODO: Add multi image verifying
    try:
        result = core.verify(args.image[0], options=options, **session_args)
        print(result)
    except Exception as e:
        print(e)


def handle_flash(args):
    """Helper function for handling 'flash' command"""
    session_args = get_session_args(args)
    images = list()
    options = dict()

    for img in args.images:
        images.append(img)

    if args.options:
        for opt in args.options:
            option_id = opt[0]
            option_value = opt[1]

            options.update({option_id: option_value})

    if len(options) == 0:
        options = None

    # TODO: Add multi image flashing
    try:
        result = core.flash(images[0], binary=args.bin, options=options,
                           address=args.address, **session_args)
        print(result)
    except Exception as e:
        print(e)


def handle_memory(args):
    """Helper function for handling 'memory' command"""
    session_args = get_session_args(args)

    if args.read:
        try:
            result = core.memory_read(args.address, args.num_bytes, args.page,
                **session_args)
            if args.hex:
                result = [ hex(h) for h in result ]
            print(result)
        except Exception as e:
            print(e)
    elif args.write:
        try:
            result = core.memory_write(args.address, args.data, args.page,
                **session_args)
        except Exception as e:
            print(e)


def handle_expression(args):
    """Helper function for handling 'expression' command"""
    session_args = get_session_args(args)

    try:
        result = core.evaluate(args.expression, symbol_file=args.symbols,
                                **session_args)
        print(result)
    except Exception as e:
        print(e)


def main(args=None):
    """Runs main TIFlash script

    Args:
        args (argparse.namespace): arguments to use for script. If no args are
        passed to main() then args will be parsed from command line.
    """
    if not args:
        args = parse_args()

    # Options
    if args.cmd == 'option':
        handle_option(args)

    # Lists
    elif args.cmd == 'list':
        handle_list(args)

    # Reset
    elif args.cmd == 'reset':
        handle_reset(args)

    # Erase
    elif args.cmd == 'erase':
        handle_erase(args)

    # Verify
    elif args.cmd == 'verify':
        handle_verify(args)

    # Flash
    elif args.cmd == 'flash':
        handle_flash(args)

    # Memory
    elif args.cmd == 'memory':
        handle_memory(args)

    # Expression
    elif args.cmd == 'evaluate':
        handle_expression(args)


if __name__ == "__main__":
    args = parse_args()
    main(args)
