import os

from tiflash.utils import cpus


class TestCPUS():
    def test_get_cpus_directory(self, t_env):
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    '/ccs_base/common/targetdb/cpus')

        result = cpus.get_cpus_directory(t_env['CCS_PATH'])

        assert result == expected

    def test_get_cpus(self, t_env):
        result = cpus.get_cpus(t_env['CCS_PATH'])

        assert type(result) is list

    def test_get_cpu_name(self, t_env):
        expected = "Cortex_M3"
        cpuxml = os.path.normpath(t_env['CCS_PATH'] +
                                  "/ccs_base/common/targetdb/cpus/"
                                  "cortex_m3.xml")

        result = cpus.get_cpu_name(cpuxml)

        assert result == expected
