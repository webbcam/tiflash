.. _session_api:

Session Arguments
=================

.. data:: **session_args

        ``**session_args`` are a set of keyword arguments (\*\*kwargs) that specify
        how to connect to a device when running a command.

        Each argument can be provided in any function that takes
        ``**session_args`` as a parameter. Just provide the particular
        argument(s) in the function call as a keyword argument:

        .. code-block:: python

            # Example of providing session args: 'serno' and 'ccs'
            function_name(serno="LXXXXXX", ccs=7)


        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | Name             | Type       | Description                                      | Default                             |
        +==================+============+==================================================+=====================================+
        | **serno**        | str        | serial number of device                          |                                     |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **devicetype**   | str        | full devicetype name                             |                                     |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **ccs**          | str        | full path to ccs installation or version number  | latest                              |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **chip**         | str        | cpu/chip of device to connect to                 | first chip found for device         |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **connection**   | str        | full name of connection to use                   | default connection for device       |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **ccxml**        | str        | full path to ccxml file to use                   |                                     |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **fresh**        | boolean    | force a new ccxml file to be created and used    | False                               |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **debug**        | boolean    | output debug information when running            | False                               |
        +------------------+------------+--------------------------------------------------+-------------------------------------+
        | **timeout**      | int        | amount of time (seconds) for tiflash to execute  | 60                                  |
        +------------------+------------+--------------------------------------------------+-------------------------------------+

----

        .. note::

            +------------------+---------------------------------------------------------------------------------------------------+
            | Name             | Tips                                                                                              |
            +==================+===================================================================================================+
            | **devicetype**   | you can see a list of devicetypes with the `get_devicetypes()                                     |
            |                  | <core.html#tiflash.core.api.get_devicetypes>`_ function                                           |
            +------------------+---------------------------------------------------------------------------------------------------+
            | **chip**         | you can see a list of chips/cpus with the `get_cpus()                                             |
            |                  | <core.html#tiflash.core.api.get_cpus>`_ function                                                  |
            +------------------+---------------------------------------------------------------------------------------------------+
            | **connection**   | you can see a list of connections with the `get_connections()                                     |
            |                  | <core.html#tiflash.core.api.get_connections>`_ function                                           |
            +------------------+---------------------------------------------------------------------------------------------------+
            | **ccxml**        | providing an existing ccxml file to use will eliminate any requirement of providing               |
            |                  | a serno, devicetype, and/or connection type                                                       |
            +------------------+---------------------------------------------------------------------------------------------------+

        .. warning::

            *At the very minimum you'll need to provide the device's serial number
            (serno) or devicetype.*

            TIFlash will try to determine the rest of the information from
            there. If a piece of information cannot be determined, an error will be
            raised and you'll need to provide this information as a session
            argument.
