.. _index:

TI-Flash Documentation
======================

An *unofficial* Python flash programmer for `TI
Launchpads <http://www.ti.com/tools-software/launchpads/overview.html>`__.

Overview
--------

**TIFlash** uses TI’s `Code Composer Studio`_ scripting interface `Debug Server
Scripting`_
to flash devices. It’s essentially a python/command line interface for
CCS. This is helpful when just needing to perform simple actions like
flashing, erasing or resetting a device without having to spin up an
entire CCS GUI session.

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
   contributing
   license

.. External Links
.. _Debug Server Scripting: http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html
.. _Code Composer Studio: http://www.ti.com/tool/CCSTUDIO
.. _Python: https://www.python.org/downloads/
