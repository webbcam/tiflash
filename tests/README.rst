=======
Testing
=======

This directory contains all necessary files for running the tests

Setting up Test Environment
===========================

To setup your testing environment, you'll need at least one device to run
tests on. Below are the devices supported out of the box that include resources
for testing (if you want to run tests on a device not listed below, you'll need
to provide similar resources for that device. See `tests/resources/cc1310 <resources/cc1310>`_ for an
example)

- `cc1310/cc1350 <resources/cc1310/README.rst>`_


Steps
-----

1. Edit the file `tests/env.cfg <env.cfg>`_

   **Minimum Requirements:**

   1. ``prefix``: full path to parent directory of CCS installations (e.g. /opt/ti)
   2. ``versions``: comma-separated list of CCS version numbers (e.g. 9.0.1.00004, 8.1.0.00011)

      a. for each version listed you'll need to provide the full path to that
         CCS installation 
         (e.g. 9.0.1.00004 = /opt/ti/ccs901/ccs)

   3. Enter the required device information (see `tests/resources/cc1310/README.rst <resources/cc1310/README.rst>`_
      for what's required)
      
   |   
   | An example:
   
   :: 
      
      # env.cfg
      [ccs]
      prefix = /opt/ti
      versions = 9.0.1.00004, 8.1.0.00011
      9.0.1.00004: /opt/ti/ccs901/ccs
      8.1.0.00011: /opt/ti/ccsv8
      
      [devices]
      cc1310
      
      [cc1310]
      serno = L20000CE

2. Configure the test setup
   ::

       # From the top level directory
       make configure

3. Run tests
   ::

       # From the top level directory
       make test
