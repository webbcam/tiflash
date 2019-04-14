import pytest
import platform
import shutil
import json
import os

SETUP_FILE = os.path.join(os.path.dirname(__file__), "env.json")

def pytest_generate_tests(metafunc):
    with open(SETUP_FILE, "r") as f:
        tsetup = json.load(f)
    if 'tdev' in metafunc.fixturenames:
        tdevlist = [tsetup[dev] for dev in tsetup["devices"]]
        metafunc.parametrize("tdev", tdevlist, scope="class")


@pytest.fixture(scope="class")
def tenv(request):
    """Fixture for accessing paths set in setup.json file"""
    with open(SETUP_FILE, "r") as f:
        tsetup = json.load(f)

    return tsetup


@pytest.fixture(autouse=True, scope="class")
def test_env_setup(request, tenv, tdev):
    if not os.path.exists(tenv["paths"]["tmp"]):
        os.makedirs(tenv["paths"]["tmp"])

    shutil.copyfile(tdev["ccxml-path"], tenv["paths"]["ccxml"]+"/"+tdev["serno"]+".ccxml")
    shutil.copyfile(tdev["ccxml-path"], tenv["paths"]["ccxml"]+"/"+tdev["devicetype"]+".ccxml")

    def teardown():
        shutil.rmtree(tenv["paths"]["tmp"])

    request.addfinalizer(teardown)
