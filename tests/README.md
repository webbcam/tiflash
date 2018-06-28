# Testing

All tests are in the [tests](tests) directory. These are the tests that are run before each pull request/merge. They are written using [pytest](https://docs.pytest.org/en/latest/) and thus you'll need to install the pytest module in order to run the tests.

## Setup
#### Requirements
Installing the [pytest](https://docs.pytest.org/en/latest/) module and [pytest-html](https://github.com/pytest-dev/pytest-html) plugin.
```
# Install pytest
pip install pytest

# Install pytest html-report plugin
pip install pytest-html
```
#### Hardware
Most tests require to be run on an actual Launchpad device. To run the tests on your local machine you'll need to connect at least one Launchpad to your PC and update the *devices.cfg* file with this device's information.
```
# devices.cfg	(see devices.cfg for example)

[Device Name]
serno=<Device Serial Number>
connection=<Connection Name>
devicetype=<Devicetype Name>
image=<Full path to a valid image hex file>
enabled=true
```
You can have multiple device entries (labeled by the [Device Name]) in your devices.cfg file. When you run any tests that interact with hardware, the test(s) will be run on each of these devices.

* **[Device Name]** - unique identifier for the device entry
* **serno** - serial number of device
* **connection** - the full connection name of the device
* **devicetype** - the full devicetype name of the device
* **image** - the full path to the device specific image (.hex file)
* **enabled** - boolean that enables/disables this device entry from being included in tests

## Core Tests

These tests cover the main functionality of the TIFlash module by testing the core layer.

```
# Test all core tests
pytest tests/core

# Test individual test
pytest tests/core/test_api_flash.py
```

## Utils Tests

These tests cover the utility/helper modules located in the tiflash/utils folder. 

```
# Test all utils tests
pytest tests/utils

# Test individual test
pytest tests/utils/test_ccsfinder.py
```

## Coding Style Tests

All code should follow [PEP8](https://www.python.org/dev/peps/pep-0008/) standards. Install the modules 'flake8' for running coding style checks before making any commits.

This is automated using the pre-commit.sh scripts in tiflash/scripts directory. You can install them by running the install-hooks.sh to setup your git repo for automatically running flake8 on any files you modify.

```
pip install -u flake8
cd tiflash/scripts
./install-hooks.sh
```
