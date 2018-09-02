.. _session:

Session
=======

There are a variety of ways for specifying a device to connect to.
Below are a list of arguments you can provide for specifying how to connect to
a device.

.. note:: You should always specify all session arguments *before* specifying the
    command you wish to execute.

.. argparse::
    :module: tiflash.core.__main__
    :func: generate_parser
    :prog: tiflash
    :nosubcommands:

.. note:: Most often you’ll only need to supply the serial number and TIFlash will
    try to automatically determine the default configurations (device type,
    connection, chip, etc.) to use when connecting to the device.
