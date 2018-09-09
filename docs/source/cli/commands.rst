.. _commands:

Commands
========

.. toctree::
    :hidden:
    :maxdepth: 1

    reset
    flash
    erase
    verify
    memory-read
    memory-write
    evaluate
    xds110-reset
    xds110-upgrade
    xds110-list
    options-get
    options-list
    attach
    list

Below is a list of commands you can call with TIFlash.

.. note:: You can only provide one command at a time. All session arguments should
    be specified before specifying the command to use.

.. container::

    :ref:`Reset <reset>`

*board reset a device*

.. container::

    :ref:`Flash <flash>`

*flash image(s) on to a device*

.. container::

    :ref:`Erase <erase>`

*erase a device's flash*

.. container::

    :ref:`Verify <verify>`

*verify an image in a device's flash*

.. container::

    :ref:`Memory-Read <memory-read>`

*read from memory location in device's flash*

.. container::

    :ref:`Memory-Write <memory-write>`

*write to memory location in device's flash*

.. container::

    :ref:`Evaluate <evaluate>`

*evaluate a C/GEL expression on a device*

.. container::

    :ref:`XDS110-Reset <xds110-reset>`

*run xds110-reset command*

.. container::

    :ref:`XDS110-Upgrade <xds110-upgrade>`

*run xds110-upgrade command*

.. container::

    :ref:`XDS110-List <xds110-list>`

*run xds110-list command*

.. container::

    :ref:`List <list>`

*list environment/device information*

.. container::

    :ref:`Options-Get <options-get>`

*get an option on a device*

.. container::

    :ref:`Options-List <options-list>`

*list options for a device*

.. container::

    :ref:`Attach <attach>`

*attach a CCS session to device*
