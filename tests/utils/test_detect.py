import pytest

from tiflash.utils import detect


class TestDetect():
    def test_detect_sernos(self, tenv):
        cfg_devicelist = tenv['devices']
        detected_devicelist = detect.detect_devices()
        detected_sernos = [ dev[2] for dev in detected_devicelist ]


        for devicename in cfg_devicelist:
            dev = tenv[devicename]
            assert dev['serno'] in detected_sernos
