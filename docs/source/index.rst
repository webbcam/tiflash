.. _index:

TI-Flash |Status| |Version|
===========================

An *unofficial* Python flash programmer for `Texas Instruments
Launchpads <http://www.ti.com/tools-software/launchpads/overview.html>`__.

----

Overview
--------

| |PyVersions| |CCSVersions| |License| |Downloads|

*TIFlash* is a python/command-line interface for Texas Instruments’ `Code Composer Studio`_.
It allows you to perform many of the operations possible in the CCS GUI via python or
command-line. This can be extremely useful for automating tasks involving Texas Instruments
microcontrollers or embedded processors. In addition, TIFlash makes it easier to perform
simple actions like flashing, erasing or resetting a device without having to spin up an
entire CCS GUI session.

Under the Hood
~~~~~~~~~~~~~~

Under the hood TIFlash uses CCS's scripting interface (`Debug Server
Scripting`_) to interact with devices.

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
   api
   cli
   examples
   contributing
   license
   disclaimer
   changelog

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

.. |CCSVersions| image:: https://img.shields.io/badge/CCStudio-v6%20|%20v7%20|%20v8%20|%20v9-blue.svg?style=flat
    :target:            http://processors.wiki.ti.com/index.php/Download_CCS
    :alt:               CCS Versions

.. |Docs| image::       https://readthedocs.org/projects/tiflash/badge/?version=latest
    :target:            https://tiflash.readthedocs.io
    :alt:               Documentation

.. |Downloads| image::  https://pepy.tech/badge/tiflash
    :target:            https://pepy.tech/project/tiflash
    :alt:               Downloads

.. |License| image::    https://img.shields.io/pypi/l/tiflash.svg?style=flat
    :target:            https://github.com/webbcam/tiflash/blob/master/LICENSE
    :alt:               License: MIT

