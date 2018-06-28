import os
import platform

try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

class TestSetupError(Exception):
    """Generic Error with parsing Test Setup configuration"""
    pass

class TestSetup(object):
    """Class used for accessing various settings in test setup configuartion
    file: setup.cfg
    """
    def __init__(self):
      self.cfg = ConfigParser(allow_no_value=True)
      self.cfg.optionxform = str
      self.cfg.read("./setup.cfg")


    def get_ccs_versions(self):
        """Returns a tuple of CCS versions installed

        Returns:
            tuple: a tuple of ints representing CCS versions installed in test
              setup
        """
        versions_str = self.cfg.get('ccs', 'versions').split(',')
        versions = map(int, versions_str)

        return tuple(versions)

    def get_ccs_installs(self):
        """Returns a tuple of all CCS install paths

        Returns:
            tuple: a tuple of strs being the full paths to each CCS
              installation
        """
        system = platform.system()
        versions = self.get_ccs_versions()

        if self.cfg.has_option('ccs', 'custom_install'):
            ccs_directory = self.cfg.get('ccs', 'custom_install')
        else:   # Determine ccs path by platform (os)
            if system == 'Windows':
                ccs_directory = "C:/ti"
            elif system == 'Linux':
                ccs_directory = os.environ['HOME'] + "/ti"
            elif system == 'Darwin':
                ccs_directory = "/Applications/ti"
            else:
                raise Exception("Unsupported platform: %s" % system)

        ccs_paths = tuple(ccs_directory + "/ccsv%d" %v for v in versions)

        for path in ccs_paths:
            if not os.path.exists(path):
              raise TestSetupError("CCS Install: %s could not be found. "
                                    "Remove this ccs version from setup.cfg"
                                    % path)
        return ccs_paths

    def get_target_config_directory(self):
        """Returns the target configuation directory

        Returns:
            str: Path to target configuration directory
        """
        system = platform.system()

        if self.cfg.has_option('ccs', 'target_configs'):
            config_directory = self.cfg.get('ccs', 'target_configs')
        else:   # Determine ccs path by platform (os)
            if system == 'Windows':
                config_directory = os.environ['USERPROFILE']
            elif system == 'Linux' or system == 'Darwin':
                config_directory = os.environ['HOME']
            else:
                raise Exception("Unsupported platform: %s" % system)

            config_directory += "/ti/CCSTargetConfigurations"

        if not os.path.exists(config_directory):
              raise TestSetupError("Target Config Directory: %s could not"
                                    " be found." % config_directory)
        return config_directory




    def get_devices():
        """Returns a dict of devices with specified configurations (devices.cfg)

        Returns:
            dict: dict of device dicts in format:
                { devicename:
                    {
                        serno: SERNO,
                        connection: CONN,
                        devicetype: DEVTYPE
                    }
                }
        """
        devices = dict()

        device_list = [ dev for dev in self.cfg.options('devices') if
          self.cfg.getboolean('devices', dev) ]

        for devname in device_list:
            dev = dict()
            options = self.cfg.options(devname)

            for o in options:
                dev[o] = self.cfg.get(devname, o)

            devices[devname] = dev

        return devices
