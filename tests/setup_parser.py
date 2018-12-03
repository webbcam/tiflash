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
        versions_str = self.cfg.get('environment', 'ccs_versions').split(',')
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

        ccs_prefix = self.cfg.get('environment', 'ccs_prefix')

        ccs_paths = tuple(ccs_prefix + "/ccsv%d" %v for v in versions)

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

        ccxml_dir = self.cfg.get("environment", "ccxml_dir")

        if not os.path.exists(ccxml_dir):
              raise TestSetupError("Target Config Directory: %s could not"
                                    " be found." % ccxml_dir)
        return ccxml_dir


    def get_devices(self):
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
