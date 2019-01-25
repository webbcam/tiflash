.. _started:

Getting Started
===============

.. contents::
    :local:
    :depth: 1

Prerequisites
-------------

You will need to have `Code Composer Studio`_ installed along with any drivers
for any devices you plan to use (offered during installation of CCS or
available in CCS’s Resource Explorer).

You’ll also need `Python`_ installed on your computer, either 2.7 or
3.6+ (preferred) will work.

Installing
----------

Install TIFlash with ``pip install tiflash``.

You can then do a quick test of your installation on the command line:

.. image:: images/started.png



.. External Links
.. _Debug Server Scripting: http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html
.. _Code Composer Studio: http://www.ti.com/tool/CCSTUDIO
.. _Python: https://www.python.org/downloads/

Configuration
-------------

Custom CCS Install Path
.......................

.. note::
    If you have CCS installed in the default directory, TIFlash should work out of
    box with no additional configurations.

If you installed CCS in a custom location, you'll need to specify
the path of the CCS installation to TIFlash. You can do this either of two ways:

Option #1
    Set the environment variable ``CCS_PREFIX`` to the parent directory of your installation:

    Example:

      If you have CCSv8 installed at the path: ``/opt/ti/ccsv8`` you would need to set ``CCS_PREFIX=/opt/ti``

    *This option is nice when you have multiple CCS installations in the same
    directory since TIFlash will look for any folders named 'ccsv[?]'*

Option #2
    Pass the full path to the ccsv folder as the ``ccs`` argument for every
    TIFlash command called.

    Example:

        ::

            tiflash.detect_devices(ccs="/opt/ti/ccsv8")
