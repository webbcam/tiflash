Contributing Guidelines
=======================

Contributions are very welcome! This includes not only code, but bug
reports and documentation. Please follow the guidelines laid out below.

When contributing to this repository, please first discuss the change
you wish to make via an “issue”. The issue will be used as a forum of
discussion for the bug, feature or update before merging the changes.

This repo follows the `Git Feature Branch
Workflow <https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow>`__
for any new features/bugs/updates.

Table of Contents
-----------------

-  `Setting up Development
   Environment <#setting-up-development-environment>`__
-  `Running Tests <#running-tests>`__
-  `Pull Request Process <#pull-request-process>`__

Setting Up Development Environment
----------------------------------

Install via git repo

::

    # clone repo
    git install https://github.com/webbcam/tiflash.git

    # install required 3rd party modules
    cd tiflash
    pip install -r requirements.txt

    # install tiflash via pip in develop mode
    pip install -e .

    # setup pre-commit hooks (style guide testing)
    cd hooks
    chmod +x install-hooks.sh pre-commit.sh
    ./install-hooks.sh

Running Tests
-------------

Before creating any pull requests you should be sure to run the tests
(located in `tests <tests>`__ directory) locally.

Prerequisites
~~~~~~~~~~~~~

You’ll need the `pytest <https://docs.pytest.org/en/latest/>`__ module
to run the tests.

::

    # install pytest
    pip install -U pytest

You’ll also need at least one device connected to your PC to run the
tests on. You’ll need to add the device(s) information to the
tests/devices.cfg file. (Also include a valid image in this
configuration file for flash tests).

Running the tests
~~~~~~~~~~~~~~~~~

All tests are located in the `tests <tests>`__ directory. Please see the
`README.md <tests/README.md>`__ in the tests directory for detailed
information on running the tests.

You are able to run any tests ranging from an entire test suite to sub
test suites to just a particular test. *(Note: upon submitting a pull
request, we will run the entire test suite before merging).*

::

    cd tiflash/tests

    # Entire Test Suite
    py.test ./

    # Sub Test Suite (i.e. core)
    py.test core/

    # Particular Test
    py.test utils/ccsfinder.py

\**Please see the README.md in the tests directory for more
information\*

Raising an Issue
----------------

Please raise an issue for any bug, new feature or updates. You should
use the `ISSUE_TEMPLATE.md <ISSUE_TEMPLATE.md>`__ as a starting place
for your issue.

Pull Requests
-------------

When preparing a pull request you should run through the following
steps:

1. Run entire test suite on your local PC with the new changes and
   include report.html (generated with pytest-html plugin) with pull
   request.
2. Update the appropriate README.md with details of changes to the
   project. This includes any new feature added, any new tests added
   (and expected result) for fixed bug, etc.
3. Increase the version numbers in any examples files and the README.md
   to the new version that this Pull Request would represent. The
   versioning scheme we use is `SemVer <http://semver.org/>`__.
4. You may merge the Pull Request in once you have the sign-off of two
   other developers, or if you do not have permission to do that, you
   may request the second reviewer to merge it for you. Note all tests
   must pass on our test setup before Pull Request can be merged.

