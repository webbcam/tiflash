.. _cc13xx-cc26xx:

.. highlight:: python

CC13XX/CC26XX
=============

.. contents::
    :local:


Below are common example commands specific for Texas Instruments' CC13XX and
CC26XX devices.

IEEE Address
------------
Obtaining a device's IEEE Address.


**Python**

.. highlight:: python

::

    >>> core.get_option("DeviceIeeePrimary", pre_operation="ReadPriIeee", serno="L4000CE")

    00:12:4B:00:11:22:33:44

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE option --get DeviceIeeePrimary --operation "ReadPriIeee"

    00:12:4B:00:11:22:33:44

BLE Address
------------
Obtaining a device's BLE Address.

**Python**

.. highlight:: python

::

    >>> core.get_option("DeviceBlePrimary", pre_operation="ReadPriBle", serno="L4000CE")

    00:81:F9:11:22:33

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE option --get DeviceBlePrimary --operation "ReadPriBle"

    00:81:F9:11:22:33

Flash Erase All
---------------
Erase entire Flash on device before flashing image.

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseSetting" : "All Unprotected Sectors"}
    >>> core.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "FlashEraseSetting" "All Unprotected Sectors"

    True

Flash Erase Necessary Sectors Only
----------------------------------
Erase Necessary Sectors Only of Flash on device before flashing image.
*NOTE: This is the default flash option and therefore you do not need to actually specify this.*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseSetting" : "Necessary Sectors Only"}
    >>> core.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "FlashEraseSetting" "Necessary Sectors Only"

    True

Flash Erase Program Load Only
-----------------------------
Program Load Only (do not erase any sectors of flash) when flashing image on to
device.

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseSetting" : "Program Load Only (do not erase sectors)"}
    >>> core.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "FlashEraseSetting" "Program Load Only (do not erase sectors)"

    True

Reset After Flash
-----------------
Reset the device after flashing.

**Python**

.. highlight:: python

::

    >>> opts = {"ResetOnRestart" : True}
    >>> core.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "ResetOnRestart" "True"

    True


Device Revision
---------------
Get device's Revision Number.

**Python**

.. highlight:: python

::

    >>> core.get_option("DeviceInfoRevision", serno="L4000CE")

    "2.1"

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE option --get DeviceInfoRevision

    2.1

Device RAM Size
---------------
Get RAM size on device.

**Python**

.. highlight:: python

::

    >>> core.get_option("DeviceInfoRAMSize", serno="L4000CE")

    "80 KB"

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE option --get DeviceInfoRAMSize

    80 KB

Device Flash Size
-----------------
Get Flash size on device.

**Python**

.. highlight:: python

::

    >>> core.get_option("DeviceInfoFlashSize", serno="L4000CE")

    "352 KB"

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE option --get DeviceInfoFlashSize

    352 KB
