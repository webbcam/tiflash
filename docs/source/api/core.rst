.. _core:

TIFlash
=======

This module contains the core functions used for interacting with
CCS. These functions are not specific to any particular device family and thus
can be used on any device.

.. code-block:: python

    # All core functions are provided in the tiflash module
    import tiflash

.. data:: **session_args

        ``**session_args`` are a set of keyword arguments (\*\*kwargs) that specify
        how to connect to a device when running a command.

        Each argument can be provided in any function that takes
        ``**session_args``. Just provide the particular argument in the function
        call as a keyword argument:

        .. code-block:: python

            # Example of providing session args: 'serno' and 'ccs'
            function_name(serno="LXXXXXX", ccs=7)

        .. warning::

            *At the very minimum you'll need to provide the device's serial number
            (serno).*

            TIFlash will try to determine the rest of the information from
            there. If a piece of information cannot be determined, an error will be
            raised and you'll need to provide this information in the session
            argument.


        serno (str):
            serial number of device

        devicetype (str, optional):
            full devicetype name

                :HINT:  you can see a list of devicetypes with the
                  `tiflash.core.api.get_devices`_ function

        ccs (int, optional):
            version of ccs to use

                :DEFAULT:   latest version of ccs installed

        chip (str, optional):
            core/chip of device to connect to

                :HINT: you can see a list of chips with the
                  `tiflash.core.api.get_cpus`_ function

        connection (str, optional):
            full name of connection to use

                :HINT: you can see a list of connections with the
                  `tiflash.core.api.get_connections`_ function

        ccxml (str, optional):
            path to a specific ccxml file to use


        fresh (boolean, optional):
            specify to create a new ccxml file (instead of using existing)

                :DEFAULT: False

        debug (boolean, optional):
            specify to output debugging info when running command

                :DEFAULT: False

        timeout (int):
            amount of time to give to execute command

                :DEFAULT: 60s


.. automodule:: tiflash.core.api
    :members:
    :undoc-members:
    :show-inheritance:
