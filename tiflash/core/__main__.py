import argparse
from platform import python_version
from pprint import pprint

import tiflash
from tiflash.core.args import (
    SessionParser,
    OptionsGetParser,
    OptionsListParser,
    ListParser,
    ResetParser,
    EraseParser,
    VerifyParser,
    FlashParser,
    MemoryReadParser,
    MemoryWriteParser,
    RegisterReadParser,
    RegisterWriteParser,
    ExpressionParser,
    AttachParser,
    XDS110ResetParser,
    XDS110UpgradeParser,
    XDS110ListParser,
    DetectParser,

    get_session_args
)

def __exit_with_error(e):
    """Helper function for printing Exception message and exiting with non-zero
    exit number

    Args:
        e (Exception): Exception raised
    """
    raise SystemExit(e)

def generate_parser():
    """Generates an argument parser

    Returns:
        argparse.ArgumentParser
    """
    full_version = "tiflash: %s - python: %s" % (tiflash.__version__, python_version())

    main_parser = argparse.ArgumentParser(prog="tiflash", parents=[SessionParser],
        usage="tiflash [session arguments] <command> [command arguments]")
    main_parser._positionals.title = "commands"
    main_parser._optionals.title = "session arguments"
    main_parser.add_argument('-v', '--version', action='version',
                        version=tiflash.__version__,
                        help='print tiflash version')
    main_parser.add_argument('-V', '--VERSION', action='version',
                        version=full_version,
                        help='print tiflash & python version')

    sub_parsers = main_parser.add_subparsers(dest='cmd')

    # Options
    sub_parsers.add_parser('options-get', parents=[OptionsGetParser],
        usage="tiflash [Session Arguments] options-get <optionID> [optionals]",
        description="Get value of a device option.")
    sub_parsers.add_parser('options-list', parents=[OptionsListParser],
        usage="tiflash [Session Arguments] options-list [optionID]",
        description="List device options.")

    # List
    sub_parsers.add_parser('list', parents=[ListParser],
        usage="tiflash [Session Arguments] list [optionals]",
        description="List device/environment information.")

    # Reset
    sub_parsers.add_parser('reset', parents=[ResetParser],
        usage="tiflash [Session Arguments] reset [optionals]",
        description="Reset a device. (Board Reset)")

    # Erase
    sub_parsers.add_parser('erase', parents=[EraseParser],
        usage="tiflash [Session Arguments] erase [optionals]",
        description="Erase a device's flash.")

    # Verify
    sub_parsers.add_parser('verify', parents=[VerifyParser],
        usage="tiflash [Session Arguments] verify [optionals]",
        description="Verify an image on a device's flash.")

    # Flash
    sub_parsers.add_parser('flash', parents=[FlashParser],
        usage="tiflash [Session Arguments] flash [optionals]",
        description="Flash a device with an image(s).")

    # Memory
    sub_parsers.add_parser('memory-read', parents=[MemoryReadParser],
        usage="tiflash [Session Arguments] memory-read <address> [optionals]",
        description="Read from memory location on a device.")
    sub_parsers.add_parser('memory-write', parents=[MemoryWriteParser],
        usage="tiflash [Session Arguments] memory-write <address> [optionals]",
        description="Write to memory location on a device.")

    # Register
    sub_parsers.add_parser('register-read', parents=[RegisterReadParser],
        usage="tiflash [Session Arguments] register-read <regname> [optionals]",
        description="Read from register on a device.")
    sub_parsers.add_parser('register-write', parents=[RegisterWriteParser],
        usage="tiflash [Session Arguments] register-write <reganame> <value>",
        description="Write value to register on a device.")

    # Evaluate
    sub_parsers.add_parser('evaluate', parents=[ExpressionParser],
        usage="tiflash [Session Arguments] evaluate <expression> [optionals]",
        description="Evaluate a C/GEL expression on a device.")

    # Attach
    sub_parsers.add_parser('attach', parents=[AttachParser],
        usage="tiflash [Session Arguments] attach",
        description="Open up CCS session & attach to device")

    # XDS110 Parsers
    sub_parsers.add_parser('xds110-reset', parents=[XDS110ResetParser],
        usage="tiflash [Session Arguments] xds110-reset",
        description="Calls xds110reset on specified device")
    sub_parsers.add_parser('xds110-upgrade', parents=[XDS110UpgradeParser],
        usage="tiflash [Session Arguments] xds110-upgrade",
        description="Upgrades XDS110 firmware on device")
    sub_parsers.add_parser('xds110-list', parents=[XDS110ListParser],
        usage="tiflash [Session Arguments] xds110-list",
        description="Lists sernos of connected XDS110 devices")

    # Detect
    sub_parsers.add_parser('detect', parents=[DetectParser],
        usage="tiflash [Session Arguments] detect",
        description="Detect devices connected to machine")


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


def handle_options(args):
    """Helper function for handling 'option' command"""
    session_args = get_session_args(args)
    # Get Option
    if args.cmd == 'options-get':
        try:
            value = tiflash.get_option(args.optionID, pre_operation=args.operation,
                                   **session_args)
            print(value)
        except Exception as e:
            __exit_with_error(e)

    # Set Option
    elif args.cmd == 'options-set':
        __exit_with_error("Setting Option is unsupported at this time")

    # Display Option Information
    elif args.cmd == 'options-list':
        options = tiflash.list_options(option_id=args.optionID, **session_args)
        header = "Options (%s):" % args.optionID if args.optionID else "Options:"
        print(header)
        print("-" * len(header))
        __print_options(options)


def __print_options(options):
    """Helper function for printing the options returned from
    tiflash.list_options() in a clean format.
    """
    ids = options.keys()
    for opt_id in ids:
        opt = options[opt_id]
        opt_keys = opt.keys()

        opt_type = opt["type"] if "type" in opt_keys else None
        opt_choices = opt["choices"] if "choices" in opt_keys else None
        opt_default = opt["default"] if "default" in opt_keys else None

        print("%s:" % opt_id)
        print("\ttype: %s" % opt_type)
        if opt_default:
            if opt_type == "Boolean":
                opt_default = opt_default == "1"
            else:
                opt_default = "\"%s\"" % opt_default
            print("\tdefault: %s" % opt_default)

        if opt_choices:
            print("\tchoices:")
            for choice in opt_choices:
                print("\t\t\"%s\"" % choice)


def handle_list(args):
    """Helper function for handling 'list' command"""
    results = []
    session_args = get_session_args(args)
    if args.devicetypes:
        results = tiflash.get_devicetypes(args.ccs, search=args.search)
    elif args.connections:
        results = tiflash.get_connections(args.ccs, search=args.search)
    elif args.cpus:
        results = tiflash.get_cpus(args.ccs, search=args.search)
    elif args.options:
        # tiflash.print_options(**session_args)
        results = tiflash.list_options(**session_args)

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
        result = tiflash.reset(options=options, **session_args)
        print(result)
    except Exception as e:
        __exit_with_error(e)


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
        result = tiflash.erase(options=options, **session_args)
        print(result)
    except Exception as e:
        __exit_with_error(e)


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
        result = tiflash.verify(args.image[0], options=options, binary=args.bin, **session_args)
        print(result)
    except Exception as e:
        __exit_with_error(e)


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
        result = tiflash.flash(images[0], binary=args.bin, options=options,
                           address=args.address, **session_args)
        print(result)
    except Exception as e:
        __exit_with_error(e)


def handle_memory(args):
    """Helper function for handling 'memory' command"""
    session_args = get_session_args(args)

    if args.cmd == 'memory-read':
        try:
            result = tiflash.memory_read(args.address, args.num_bytes, args.page,
                **session_args)
            if args.hex:
                result = [ hex(h) for h in result ]
            print(result)
        except Exception as e:
            __exit_with_error(e)
    elif args.cmd == 'memory-write':
        try:
            result = tiflash.memory_write(args.address, args.data, args.page,
                **session_args)
        except Exception as e:
            __exit_with_error(e)


def handle_register(args):
    """Helper function for handling 'register' command"""
    session_args = get_session_args(args)

    if args.cmd == 'register-read':
        try:
            result = tiflash.register_read(args.regname, **session_args)
            if args.hex:
                result = hex(result)
            print(result)
        except Exception as e:
            __exit_with_error(e)
    elif args.cmd == 'register-write':
        try:
            result = tiflash.register_write(args.regname, args.value,
                **session_args)
        except Exception as e:
            __exit_with_error(e)


def handle_expression(args):
    """Helper function for handling 'expression' command"""
    session_args = get_session_args(args)

    try:
        result = tiflash.evaluate(args.expression, symbol_file=args.symbols,
                                **session_args)
        print(result)
    except Exception as e:
        __exit_with_error(e)


def handle_attach(args):
    """Helper function for handling 'attach' command"""
    session_args = get_session_args(args)

    try:
        result = tiflash.attach(**session_args)
    except Exception as e:
        __exit_with_error(e)


def handle_xds110(args):
    """Helper function for handling 'xds110' command"""
    session_args = get_session_args(args)

    if args.cmd == 'xds110-reset':
        try:
            result = tiflash.xds110_reset(**session_args)
            print(result)
        except Exception as e:
            __exit_with_error(e)

    elif args.cmd == 'xds110-list':
        try:
            result = tiflash.xds110_list(**session_args)
            header = "XDS110 Devices:"
            print(header)
            print('-' * len(header))
            for dev in result:
                print("%s (%s)" % (dev[0], dev[1]))
        except Exception as e:
            __exit_with_error(e)
    elif args.cmd == 'xds110-upgrade':
        try:
            result = tiflash.xds110_upgrade(**session_args)
            print(result)
        except Exception as e:
            __exit_with_error(e)


def handle_detect(args):
    """Helper function for handling 'detect' command"""
    session_args = get_session_args(args)

    try:
        result = tiflash.detect_devices(**session_args)
        header = "Detected Devices:"
        print(header)
        print('-' * len(header))
        for i, dev in enumerate(result):
            print("Connection:\t%s" % dev['connection'])
            print("Devicetype:\t%s" % (dev['devicetype'] or "N/A"))
            print("Serno:\t\t%s\n" % (dev['serno'] or "N/A"))
    except Exception as e:
        __exit_with_error(e)


def main(args=None):
    """Runs main TIFlash script

    Args:
        args (argparse.namespace): arguments to use for script. If no args are
        passed to main() then args will be parsed from command line.
    """
    if not args:
        args = parse_args()

    # Options
    if args.cmd == 'options-get' \
        or args.cmd == 'options-list':
        handle_options(args)

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
    elif args.cmd == 'memory-read' \
        or args.cmd == 'memory-write':
        handle_memory(args)

    # Register
    elif args.cmd == 'register-read' \
        or args.cmd == 'register-write':
        handle_register(args)

    # Expression
    elif args.cmd == 'evaluate':
        handle_expression(args)

    # Attach
    elif args.cmd == 'attach':
        handle_attach(args)

    # XDS110
    elif args.cmd == 'xds110-reset' \
        or args.cmd == 'xds110-upgrade' \
        or args.cmd == 'xds110-list':
        handle_xds110(args)

    # Detect
    elif args.cmd == 'detect':
        handle_detect(args)


if __name__ == "__main__":
    args = parse_args()
    main(args)
