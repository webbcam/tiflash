"""Configures test environment by setting up the 'test.json' file with your
    test environment paths and device configurations.

    Warning:
        Before running this script, you must edit the setup.cfg file in
        the tests/ directory.

    Warning:
        This script must be run once before running any tests.
"""
import os
import platform
import argparse
from jinja2 import Template
import json

try:
    from ConfigParser import ConfigParser  # Python2
except ImportError:
    from configparser import ConfigParser  # Python3


DEFAULT_ENV_CFG = "env.cfg"
DEFAULT_SETUP = "env.json"


def cfg_to_dict(cfg_path):
    """Reads in a cfg file and converts to a dict

    Args:
        cfg_path (str): full path to .cfg file to read
    Returns:
        OrderedDict: returns ordered dictionary representing .cfg file
    """
    d = dict()
    cfg = ConfigParser(allow_no_value=True)
    cfg.read(cfg_path)
    for s in cfg.sections():
        d[s] = dict(cfg.items(s))

    return d


def get_repo_path():
    """Returns the full path to the repo directory"""
    repo_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    return os.path.abspath(repo_dir)


def get_home_path():
    """Returns user's HOME path"""
    system = platform.system()

    HOME_VAR = 'USERPROFILE' if system == 'Windows' else 'HOME'
    return os.environ[HOME_VAR]


def get_root_path():
    """Returns system's ROOT path"""
    system = platform.system()
    root_path = ""
    if system == 'Windows':
        root_path = os.environ['SYSTEMDRIVE']
    elif system == 'Linux':
        root_path = os.environ['HOME']
    elif system == 'Darwin':
        root_path = '/Applications'
    else:
        raise Exception("Unsupported Operating System: %s" % system)

    return root_path

def render_j2_to_file(j2_file, output=None, **kwargs):
    """Renders the .j2 file with the provided kwargs

    Args:
        j2_file (str): full path to .j2 file
        output (str): full path to output rendering to (default is same name as
            j2 file without the .j2 extension)
        **kwargs: key word arguments to pass to render function
    """
    # Remove the .j2 extension if an output name not provided
    outf = output or j2_file.split(".j2")[0]
    with open(j2_file) as f:
        Template(f.read()).stream(**kwargs).dump(outf)


def render_j2_to_dict(j2_file, **kwargs):
    """Renders the .json.j2 file with the provided kwargs to a dict

    Args:
        j2_file (str): full path to .j2 file
        **kwargs: key word arguments to pass to render function
    """
    j2str = None
    with open(j2_file) as f:
        j2str = Template(f.read()).render(**kwargs)

    return json.loads(j2str)


def configure_setup(envcfg):
    """Configures setup.cfg file based off of the provided or env.cfg settings
        Args:
            envcfg (str): full path to the env.cfg file
    """
    env = cfg_to_dict(envcfg)
    if 'paths' not in env.keys():
        env['paths'] = dict()

    # convert ccs versions to list
    env['ccs']['versions'] = [ v.strip() for v in env['ccs']['versions'].split(',') ]
    env['paths']['ccs'] = env['ccs'][env['ccs']['versions'][0]] # take first ccs version to be default ccs path

    env["paths"]["repo"] = get_repo_path()
    env["paths"]["home"] = get_home_path()
    env["paths"]["root"] = get_root_path()
    env["devices"] = [k for k in env["devices"].keys()]

    # Set setup.json paths
    setup_cfg = os.path.join(get_repo_path(), "tests", DEFAULT_SETUP)
    setup_cfg_j2 = os.path.join(
        get_repo_path(), "tests", "resources", "templates", DEFAULT_SETUP + ".j2"
    )

    # Render the setup.json file to a dict
    setup_dict = render_j2_to_dict(setup_cfg_j2, env=env)
    env.update(setup_dict)

    # Render all j2 device files
    for dev in env["devices"]:
        j2files = [
            os.path.join(env["paths"]["resources"], dev, j2)
            for j2 in os.listdir(os.path.join(env["paths"]["resources"], dev))
            if j2.endswith(".j2")  # and not j2.startswith("setup")
        ]

        for j2 in j2files:
            if os.path.basename(j2).startswith("setup"):
                device_setup = render_j2_to_dict(j2, env=env)
                env.update(device_setup)

            else:
                render_j2_to_file(j2, env=env)

    # write to setup.json
    with open(setup_cfg, "w") as f:
        json.dump(env, f, indent=4)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cfg",
        help="full path to env.cfg file to use (default = %s)" % DEFAULT_ENV_CFG,
        type=str,
        default=None,
    )

    args = parser.parse_args()
    env_cfg_path = args.cfg or os.path.join(get_repo_path(), "tests", DEFAULT_ENV_CFG)

    configure_setup(env_cfg_path)


if __name__ == "__main__":
    main()
