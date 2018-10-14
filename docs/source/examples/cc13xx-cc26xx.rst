.. _cc13xx-cc26xx:

.. highlight:: python

CC13XX + CC26XX
===============

Below are common example commands specific for Texas Instruments' CC13XX and
CC26XX devices.

.. contents::
    :local:


IEEE Address
------------
*Obtaining a device's IEEE Address*


**Python**

.. highlight:: python

::

    >>> tiflash.get_option("DeviceIeeePrimary", pre_operation="ReadPriIeee", serno="L4000CE")

    00:12:4B:00:11:22:33:44

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE options-get DeviceIeeePrimary --operation "ReadPriIeee"

    00:12:4B:00:11:22:33:44

BLE Address
------------
*Obtaining a device's BLE Address*

**Python**

.. highlight:: python

::

    >>> tiflash.get_option("DeviceBlePrimary", pre_operation="ReadPriBle", serno="L4000CE")

    00:81:F9:11:22:33

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE options-get DeviceBlePrimary --operation "ReadPriBle"

    00:81:F9:11:22:33

Flash Erase - All Unprotected Sectors
-------------------------------------
*Erase entire Flash on device before flashing image*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseSetting" : "All Unprotected Sectors"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "FlashEraseSetting" "All Unprotected Sectors"

    True

Flash Erase - Necessary Sectors Only
------------------------------------
*Erase Necessary Sectors Only of Flash on device before flashing image (default option)*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseSetting" : "Necessary Sectors Only"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "FlashEraseSetting" "Necessary Sectors Only"

    True

Flash Erase - Program Load Only
-------------------------------
*Program Load Only (do not erase any sectors of flash) when flashing image on to device*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseSetting" : "Program Load Only (do not erase sectors)"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "FlashEraseSetting" "Program Load Only (do not erase sectors)"

    True

Reset After Flash
-----------------
*Reset the device after flashing*

**Python**

.. highlight:: python

::

    >>> opts = {"ResetOnRestart" : True}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="L4000CE")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE flash "/path/to/image.hex" -o "ResetOnRestart" "True"

    True


Device Revision
---------------
*Get device's Revision Number*

**Python**

.. highlight:: python

::

    >>> tiflash.get_option("DeviceInfoRevision", serno="L4000CE")

    "2.1"

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE options-get DeviceInfoRevision

    2.1

Device RAM Size
---------------
*Get RAM size on device*

**Python**

.. highlight:: python

::

    >>> tiflash.get_option("DeviceInfoRAMSize", serno="L4000CE")

    "80 KB"

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE options-get DeviceInfoRAMSize

    80 KB

Device Flash Size
-----------------
*Get Flash size on device*

**Python**

.. highlight:: python

::

    >>> tiflash.get_option("DeviceInfoFlashSize", serno="L4000CE")

    "352 KB"

**CLI**

.. highlight:: console

::

    $ tiflash -s L4000CE options-get DeviceInfoFlashSize

    352 KB
