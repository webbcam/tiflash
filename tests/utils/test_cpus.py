import os

from tiflash.utils import cpus


class TestCPUS():
    def test_get_cpus_directory(self, tenv):
        expected = os.path.normpath(tenv['paths']['ccs'] +
                                    '/ccs_base/common/targetdb/cpus')

        result = cpus.get_cpus_directory(tenv['paths']['ccs'])

        assert result == expected

    def test_get_cpus(self, tenv):
        result = cpus.get_cpus(tenv['paths']['ccs'])

        assert type(result) is list

    def test_get_cpu_name(self, tenv):
        expected = "Cortex_M3"
        cpuxml = os.path.normpath(tenv['paths']['ccs'] +
                                  "/ccs_base/common/targetdb/cpus/"
                                  "cortex_m3.xml")

        result = cpus.get_cpu_name(cpuxml)

        assert result == expected
