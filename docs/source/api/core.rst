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
        ``**session_args`` as a parameter. Just provide the particular
        argument(s) in the function call as a keyword argument:

        .. code-block:: python

            # Example of providing session args: 'serno' and 'ccs'
            function_name(serno="LXXXXXX", ccs=7)

        .. warning::

            *At the very minimum you'll need to provide the device's serial number
            (serno).*

            TIFlash will try to determine the rest of the information from
            there. If a piece of information cannot be determined, an error will be
            raised and you'll need to provide this information as a session
            argument.


        :Required:  - **serno** *(str)* - serial number of device

        :Optional:  - **devicetype** *(str)* - full devicetype name

                        * *HINT*: you can see a list of devicetypes with the `tiflash.core.api.get_devices`_ function

                    - **ccs** *(int)* - version of ccs to use

                        * *DEFAULT*: latest version of ccs installed

                    - **chip** *(str)* - cpu/chip of device to connect to

                        * *HINT*: you can see a list of chips with the `tiflash.core.api.get_cpus`_ function

                    - **connection** *(str)* - full name of connection to use

                        * *HINT*: you can see a list of connections with the `tiflash.core.api.get_connections`_ function

                    - **ccxml** *(str)* - path to a specific ccxml file to use

                        * *HINT*: providing an existing ccxml file removes the need to provide the device's serno

                    - **fresh** *(boolean)* - specify to create a new ccxml file (instead of using an existing one)

                        * *DEFAULT*: False

                    - **debug** *(boolean)* - specify to output info when running command

                        * *DEFAULT*: False

                    - **timeout** *(int)* - specify amount of time (seconds) for tiflash to execute a command

                        * *DEFAULT*: 60

.. automodule:: tiflash.core.api
    :members:
    :undoc-members:
    :show-inheritance:
