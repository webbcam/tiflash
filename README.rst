TI-Flash
========

An *unofficial* Python flash programmer for `Texas Instruments
Launchpads <http://www.ti.com/tools-software/launchpads/overview.html>`__.

Read The Docs
-------------

Please see the `readthedocs page <https://tiflash.readthedocs.io>`__ for the
most up to date documentation.


Getting Started
---------------

TIFlash uses Texas Instruments’s Code Composer Studio scripting interface (`Debug Server
Scripting <http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html>`__)
to flash devices. It’s essentially a python/command line interface for
CCS. This is helpful when just needing to perform simple actions like
flashing, erasing or resetting a device without having to spin up an
entire CCS GUI session.

Follow the steps below to get TIFlash set up on your computer.


Prerequisites
~~~~~~~~~~~~~

You will need to have `Code Composer
Studio <http://www.ti.com/tool/CCSTUDIO>`__ installed along with drivers
for any devices you plan to use (offered during installation of CCS or
available in CCS’s Resource Explorer).

You’ll also need `Python <https://www.python.org/>`__
installed on your computer, either 2.7 or 3.6+ (preferred) will work.


Installing
~~~~~~~~~~

Install TIFlash via PyPi (*recommended*)

::

    pip install tiflash

Install via git repo (used for development)

::

    git install https://github.com/webbcam/tiflash.git
    cd tiflash
    pip install -r requirements.txt
    pip install -e .

Quickstart
~~~~~~~~~~

TIFlash can be used via Python directly or using the commandline.

Command Line
^^^^^^^^^^^^

Installing TIFlash via pip will install the commandline application.

From a command prompt:

::

    tiflash -h      # display help menu
    tiflash -s L4000CE flash /path/to/image.hex -o ResetOnRestart True

For more commandline examples see the `EXAMPLES.rst <EXAMPLES.rst>`__ file

Python
^^^^^^

TIFlash can also be used directly in your Python scripts.

::

    import tiflash
    tiflash.flash(serno='L4000CE', image='/path/to/image.hex', options={'ResetOnRestart':True})

For more python examples see the `EXAMPLES.rst <EXAMPLES.rst>`__ file

Contributing
------------

Please read `CONTRIBUTING.rst <CONTRIBUTING.rst>`__ for details on the
process for submitting pull requests to us.

Versioning
----------

For the versions available, see the `tags on this
repository <https://github.com/webbcam/tiflash/tags>`__.

Authors
-------

-  **Cameron Webb** - *Initial work* -
   `webbcam <https://github.com/webbcam>`__

See also the list of
`contributors <https://github.com/webbcam/tiflash/contributors>`__ who
participated in this project.

License
-------

This project is licensed under the MIT License - see the
`LICENSE <LICENSE>`__ file for details

Disclaimer
----------

Please see the `Disclaimer <DISCLAIMER>`__.

Acknowledgments
---------------

-  `Debug Server
   Scripting <http://software-dl.ti.com/ccs/esd/documents/users_guide/sdto_dss_handbook.html>`__

