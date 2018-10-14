.. _cc32xx:

.. highlight:: python

CC3220/S/SF
===========

Below are common example commands specific for Texas Instruments' CC3220/S/SF devices

.. contents::
    :local:


Reset After Flash
-----------------
*Reset the device after flashing*

**Python**

.. highlight:: python

::

    >>> opts = {"ResetOnRestart" : True}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "ResetOnRestart" "True"

    True

Flash Program Option - Necessary Pages Only
-------------------------------------------
*Erase necessary pages only (default option)*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashProgramOption" : "Necessary Pages Only"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "FlashProgramOption" "Necessary Pages Only"

    True


Flash Program Option - Erase Options Specified in FlashEraseType
----------------------------------------------------------------
*Use Erase Options specified in FlashEraseType*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashProgramOption" : "Use the Erase Options Specified Below"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "FlashProgramOption" "Use the Erase Options Specified Below"

    True

Flash Program Option - Do Not Erase Flash Memory
------------------------------------------------
*Do not erase Flash Memory*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashProgramOption" : "Do Not Erase Flash Memory"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "FlashProgramOption" "Do Not Erase Flash Memory"

    True

Flash Erase Type - Entire Flash
-------------------------------
*Erase the Entire Flash (default option)*

.. warning::

    *FlashProgramOption* must be set to *"Use the Erase Options Specified Below"* in order for this setting to be used


**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseType" : "Entire Flash"}
    >>> opts["FlashProgramOption"] = "Use the Erase Options Specified Below"
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "FlashEraseType" "Entire Flash" -o "FlashProgramOption" "Use the Erase Options Specified Below"

    True

Flash Erase Type - By Address Range
-----------------------------------
*Erase Flash by specified Address Range*

.. warning::

    *FlashProgramOption* must be set to *"Use the Erase Options Specified Below"* in order for this setting to be used

.. note::

    Address Range is set by the *FlashEraseEndAddr* and *FlashEraseStartAddr* options

**Python**

.. highlight:: python

::

    >>> opts = {"FlashEraseType" : "By Address Range"} : }
    >>> opts["FlashProgramOption"] = "Use the Erase Options Specified Below"
    >>> opts["FlashEraseStartAddr"] = 0
    >>> opts["FlashEraseEndAddr"] = 0xFFFF
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "FlashEraseType" "By Address Range" -o "FlashProgramOption" "Use the Erase Options Specified Below" -o "FlashEraseStartAddr" 0 -o "FlashEraseEndAddr" 0xFFFF

    True

Flash Crystal Frequency
-----------------------
*Set the Flash Crystal Frequency*

**Python**

.. highlight:: python

::

    >>> opts = {"FlashCrystalFreq" : "8"}
    >>> tiflash.flash("/path/to/image.hex", options=opts, serno="E0071009")

    True

**CLI**

.. highlight:: console

::

    $ tiflash -s E0071009 flash "/path/to/image.hex" -o "FlashCrystalFreq" "8"

    True
