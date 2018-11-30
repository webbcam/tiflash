.. _examples:

Device Examples
===============

Each device type will have specific options you can specify when performing an
action in tiflash. These options are the same options available in the CCS
GUI.

This page attempts to cover some of the more common options used for a few of these device types.

.. note::
    Note that tiflash will work with any device that can be
    used in CCS! The devices listed below are just a few examples.

*You can view the available options for a particular device by running:*

::

    tiflash -d DEVICETYPE options-list

.. toctree::
    :caption: Device Families
    :maxdepth: 1

    examples/msp432
    examples/cc32xx
    examples/cc13xx-cc26xx
