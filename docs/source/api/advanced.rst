.. _advanced:

========
Advanced
========

.. py:module:: tiflash

This API exists for users that want more control of their device e.g. to run multiple commands on the same device over a period of time.
Using a :py:class:`TIFlashSession` object, a session can be opened for a device for sending commands.

.. toctree::
    :maxdepth: 1

    advanced/tiflashsession
    advanced/core

.. code-block:: python

   # Example
   from tiflash import TIFlashSession

   dev = TIFlashSession(serno="L2000CE")
   m3 = dev.get_core("Cortex_M3")   # gets a DeviceCore object for the device's "Cortex_M3" core

   m3.connect()
   m3.erase()
   m3.flash("/path/to/image.hex")
   val = m3.read_memory(0x2000)
   m3.disconnect()

