import os
import platform

from tiflash.utils import dss


if platform.system() == 'Windows':
    eclipsec = 'eclipsec.exe'
elif platform.system() == 'Darwin':
    eclipsec = "Ccstudio.app/Contents/MacOS/ccstudio"
else:
    eclipsec = 'ccstudio'


class TestDSS():

    def test_find_dss(self, t_env):
        expected = os.path.normpath(t_env['CCS_INSTALLS'][0] +
                                    "/eclipse/" + eclipsec)

        result = dss.find_dss(t_env['CCS_INSTALLS'][0])

        assert result == expected

    def test_call_dss(self, t_env):
        expected = (True, '')
        dss_path = os.path.normpath(t_env['CCS_INSTALLS'][0] +
                                    "/eclipse/" + eclipsec)

        result = dss.call_dss(dss_path, [])

        assert result == expected
