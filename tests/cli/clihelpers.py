"""Helper functions for testing tiflash cli"""


def get_cmd_with_device_params(device):
    """Helper function for getting cmd list with session set for device"""
    cmd = ["tiflash"]
    if "serno" in device.keys():
        cmd.extend(["--serno", '"%s"' % device["serno"]])
    cmd.extend(["--devicetype", '"%s"' % device["devicetype"]])
    cmd.extend(["--connection", '"%s"' % device["connection"]])

    return cmd
