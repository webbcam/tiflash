.. _cli:

Command-Line Interface
======================

The command-line interface is a quick and easy way to interact with a
device.


:ref:`Session Arguments <session>`
    Arguments for specifying how to connect to a device

:ref:`Commands <commands>`
    Arguments for specifying actions to perform on a device

----

.. note::

    Before getting into the various command-line arguments, it’s important to
    understand the general format for commands.

::

    # The typical format of a tiflash command is of the following:
    tiflash [session arguments] <command> [command arguments]


:tiflash: Command for invoking the command-line tool.

:session arguments: These are the arguments provided to specify which device to connect to and
                how to connect to it. *At the very least you'll need to provide the
                device's serial number.*

                *See* :ref:`Session Arguments <session>` *for a complete list of session
                arguments.*

:command:   This is the command or action to perform on the device.

        *See* :ref:`Commands <commands>` *for a complete list of commands.*

:command arguments:  These arguments are specific to each command. To see all possible options
            you can run the command with the -h help option.

            *You can view each command's specific arguments here* :ref:`Commands
            <commands>`.



.. toctree::
    :hidden:
    :maxdepth: 1

    cli/session
    cli/commands
