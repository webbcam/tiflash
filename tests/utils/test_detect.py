import pytest

from tiflash.utils import detect


class TestDetect():
    def test_detect_sernos(self, t_env):
        cfg_devicelist = t_env['DEVICES']
        detected_devicelist = detect.detect_devices()
        detected_sernos = detect.detect_sernos()

        for devicename in cfg_devicelist:
            dev = cfg_devicelist[devicename]
            assert dev['serno'] in detected_sernos
