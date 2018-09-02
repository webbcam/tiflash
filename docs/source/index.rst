.. _index:

TI-Flash Documentation
======================

An *unofficial* Python flash programmer for `Texas Instruments
Launchpads <http://www.ti.com/tools-software/launchpads/overview.html>`__.

Overview
--------

*TIFlash* is a python/command-line interface for Texas Instruments’ `Code Composer Studio`_.
It uses CCS's scripting interface (`Debug Server
Scripting`_) to flash devices. This is extremely useful for python scripts/test automation using Texas
Instruments devices. In addition, TIFlash makes it easier to perform simple actions
like flashing, erasing or resetting a device without having to spin up an entire
CCS GUI session.

.. Features
.. --------

.. Use Cases
.. ---------

Contents
--------

.. toctree::
   :maxdepth: 2
   :includehidden:

   started
   cli
   api
   examples
   contributing
   license
   disclaimer

.. External Links
.. _Debug Server Scripting: http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html
.. _Code Composer Studio: http://www.ti.com/tool/CCSTUDIO
.. _Python: https://www.python.org/downloads/
