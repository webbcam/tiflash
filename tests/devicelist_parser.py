try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser


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
    devcfg = ConfigParser()
    devcfg.read("./devices.cfg")

    devices = dict()

    device_list = devcfg.sections()

    for devname in device_list:
        dev = dict()
        options = devcfg.options(devname)

        for o in options:
            if o == 'enabled':
                val = devcfg.getboolean(devname, o)
            else:
                val = devcfg.get(devname, o)

            dev[o] = val

        if dev['enabled']:
            devices[devname] = dev

    return devices
