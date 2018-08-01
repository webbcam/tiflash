.. _cli:

Command-Line Interface
======================

The command line interface allows you to interact with a device very easily.

Command Format
--------------

Before getting into the various commandline arguments, it’s important to
note the general format for commands.

::

    # The typical format of a tiflash command is of the following:
    tiflash [CONNECTION ARGS] <ACTION> [ACTION ARGS]


    CONNECTION ARGS - you'll first want to provide any connection arguments. These can consist of:
        Serial Number   (-s): The target device serial number to perform action on
        Devicetype      (-d): The device type of the target device
        Connection      (-c): The connection type of the target device
        CCXML           (--ccxml): The full path to an existing ccxml file to use (can replace need for Serial Number)
        Chip            (--chip): The cpu/chip to connect to
        Debug           (--debug): Turn on debugging output
        CCS             (--ccs): Specify CCS version to use

    ACTIONS - action to perform on the device
        flash   : flash a device with an image(s)
        erase   : erase flash on a device
        reset   : reset device
        verify  : verify an image in device's flash
        option  : get/set an option
        list    : list device information

    ACTION ARGS - arguments specific to given ACTION. Run -h after specifying an action to see all arguments specific to that action.

Display Helpscreen
------------------

The Helpscreen is where you can view all the possible parameters and
commands to use with the TIFlash CLI

::

    # Display help screen
    $ tiflash --help

    usage: TIFlash [-h] [-s SERNO] [-d DEVICETYPE] [--ccs CCS] [--ccxml CCXML]
                   [--connection CONNECTION] [--chip CHIP] [-F] [-D]
                   {option,list,reset,erase,verify,flash} ...

    positional arguments:
      {option,list,reset,erase,verify,flash}
                            commands

    optional arguments:
      -h, --help            show this help message and exit
      -s SERNO, --serno SERNO
                            serial number of device
      -d DEVICETYPE, --devicetype DEVICETYPE
                            devicetype of device
      --ccs CCS             version (int) of ccs to use (default=latest)
      --ccxml CCXML         ccxml (full path) file to use
      --connection CONNECTION
                            connection type to use for device
      --chip CHIP           core to use
      -F, --fresh           generate new (fresh) ccxml
      -D, --debug           display debugging output

Connection Options
-----------------------------

There are a variety of ways for specifying a device to connect to.

Most often you’ll only need to supply the serial number and TIFlash will
try to automatically determine the default configurations (device type,
connection, chip, etc.) to use when connecting to the device.

::

    # Connecting to a device by serno
    $ tiflash -s <SERNO>

However occasionally you may have to specify these configurations
explicitly.

::

    # Connecting to a device and specifying device type
    $ tiflash -s <SERNO> --devicetype <DEVICETYPE>

    # Connecting to a device and specifying connection type
    $ tiflash -s <SERNO> --connection <CONNECTION NAME>

    # Connecting to a device and specifying the chip type
    $ tiflash -s <SERNO> --chip <CHIP NAME>

You can also specify an existing ccxml file to use for connecting to a
device

::

    # Connect to a device specified in a ccxml file
    $ tiflash --ccxml /path/to/device.ccxml

    # Connect to a device specified in a ccxml file and override the connection type
    $ tiflash --ccxml /path/to/device.ccxml --connection <CONNECTION NAME>

*After specifying a configuration explicitly once (i.e. connection
type), the change will persist and thus you’ll only have to specify the
serial number the next time. (Using **–fresh** will reset to defaults)*

Commands
--------

Flash
^^^^^

::

    # Flash a device
    $ tiflash -s L4000CE flash /path/to/image.hex

    # Flash a device and reset upon loading
    $ tiflash -s L4000CE flash /path/to/image.hex -o ResetOnRestart true

Erase
^^^^^

::

    # Erase a device's flash
    $ tiflash -s L4000CE erase

Reset
^^^^^

::

    # Reset a device
    $ tiflash -s L4000CE reset

Verify Image
^^^^^^^^^^^^

::

    # Verify an image in device's flash
    $ tiflash verify /path/to/image.hex

Memory
^^^^^^

::

    # Read to a device's memory
    $ tiflash memory --read --address 0x500012F0 --num 8 --hex

    # Write to a device's memory
    $ tiflash memory --write --address 0x500012F0 --data 0x01 0x02 0x03

Get Option Value
^^^^^^^^^^^^^^^^

::

    # Get Device's HW Revision (option)
    $ tiflash -s L4000CE option --get DeviceInfoRevision

    # Get Device option but running an operation prior
    $ tiflash -s L4000CE option --get DeviceBlePrimary -op ReadPriBle

List Information
^^^^^^^^^^^^^^^^

::

    # List all installed devicetypes
    tiflash list --devices

    # List all installed connections
    tiflash list --connections

    # List all installed cpus
    tiflash list --cpus

    # List all installed target configurations
    tiflash list --cfgs

Miscellaneous
-------------

Set CCS Version
^^^^^^^^^^^^^^^

::

    # Run a command using a specific CCS version
    $ tiflash --ccs 8 -s L4000CE reset

Set Debug Mode
^^^^^^^^^^^^^^

::

    # Run a command with Debug output on
    $ tiflash --debug -s L4000CE reset

Fresh CCXML
^^^^^^^^^^^

::

    # Create a fresh CCXML
    $ tiflash -s L4000CE --fresh

    # Create a fresh CCXML
    $ tiflash --ccxml /path/to/device.ccxml --fresh

