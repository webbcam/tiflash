import pytest
import platform
import shutil
import os
import setup_parser

test_setup = setup_parser.TestSetup()
ALL_DEVICES = test_setup.get_devices()

# def pytest_addoption(parser):
#    parser.addoption("--devicetype", action="append", default=None,
#        help="list of devicetypes to run tests on (default will be all)")
#
# def pytest_generate_tests(metafunc):
#    if 'devicetype' in metafunc.fixturenames:
#        device_list = metafunc.config.getoption("devicetype") or ALL_DEVICES
#        metafunc.parametrize("devicetype", device_list)


@pytest.fixture(params=ALL_DEVICES.keys(), ids=ALL_DEVICES.keys())
def device(request):
    """Test fixture that returns a dict with device specific configurations (as
    specified in devices.cfg

    By default will run any test that uses this fixture for each device in
    devices.cfg. You can specifiy to just run for one particular device with
    the '-k' cmd line parameter.

    Returns:
        dict: dictionary of device specific configs
    """
    devicename = request.param
    device = ALL_DEVICES[devicename]
    device['devicename'] = devicename

    return device


@pytest.fixture(scope='module')
def t_env(request):
    """Puts any common testing environment variables
    necessary for test cases
    """
    env = dict()
    system = platform.system()

    env['TEST_DIR'] = os.path.normpath(os.path.dirname(__file__))
    env['RESOURCE_DIR'] = os.path.normpath(env['TEST_DIR'] + '/resources')
    env['TEMP_DIR'] = os.path.normpath(env['TEST_DIR'] + '/temp')

    HOME_VAR = 'USERPROFILE' if system == 'Windows' else 'HOME'
    env['HOME_PATH'] = os.environ[HOME_VAR]

    if system == 'Windows':
        env['ROOT_PATH'] = os.environ['SYSTEMDRIVE']
    elif system == 'Linux':
        env['ROOT_PATH'] = os.environ['HOME']
    elif system == 'Darwin':
        env['ROOT_PATH'] = '/Applications'
    else:
        raise Exception("Unsupported Operating System: %s" % system)

    env['TARGET_CONFIG_PATH'] = test_setup.get_target_config_directory()


#    env['TARGET_CONFIG_PATH'] = os.path.normpath(
#        env['HOME_PATH'] + "/ti/CCSTargetConfigurations")

#    env['CCS_PATH'] = os.path.normpath(env['ROOT_PATH'] + '/ti/ccsv' + CCSV)

    env['CCS_INSTALLS'] = test_setup.get_ccs_installs()
    env['CCS_VERSIONS'] = test_setup.get_ccs_versions()

    # Environment Setup
    def setup():
        if not os.path.exists(env['TEMP_DIR']):
            os.mkdir(env['TEMP_DIR'])
    setup()

    # Environment Teardown
    def teardown():
        if os.path.exists(env['TEMP_DIR']):
            shutil.rmtree(env['TEMP_DIR'])
    request.addfinalizer(teardown)

    return env
