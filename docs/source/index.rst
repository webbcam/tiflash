.. _index:

TI-Flash |Status| |Version|
===========================

An *unofficial* Python flash programmer for `Texas Instruments
Launchpads <http://www.ti.com/tools-software/launchpads/overview.html>`__.

----

Overview
--------

| |PyVersions| |CCSVersions| |License|

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

.. Badges:

.. |Version| image::    https://img.shields.io/pypi/v/tiflash.svg?label=latest
    :target:            https://pypi.org/project/tiflash/#history
    :alt:               Version

.. |Status| image::     https://img.shields.io/pypi/status/tiflash.svg
    :target:            https://pypi.org/project/tiflash/
    :alt:               Status

.. |PyVersions| image:: https://img.shields.io/pypi/pyversions/tiflash.svg?
    :target:            https://pypi.org/project/tiflash/#files
    :alt:               Python Versions

.. |CCSVersions| image:: https://img.shields.io/badge/CCStudio-7.3%20|%207.4%20|%208.0%20|%208.1%20|%208.2-blue.svg?style=flat
    :target:            http://processors.wiki.ti.com/index.php/Download_CCS
    :alt:               CCS Versions

.. |Docs| image::       https://readthedocs.org/projects/tiflash/badge/?version=latest
    :target:            https://tiflash.readthedocs.io
    :alt:               Documentation

.. |License| image::    https://img.shields.io/pypi/l/tiflash.svg?style=flat
    :target:            https://github.com/webbcam/tiflash/blob/master/LICENSE
    :alt:               License: MIT

