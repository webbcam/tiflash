import os

from tiflash.utils import connections


class TestConnections():
    def test_get_connections_directory(self, t_env):
        expected = os.path.normpath(t_env['CCS_PATH'] +
                                    '/ccs_base/common/targetdb/connections')

        result = connections.get_connections_directory(t_env['CCS_PATH'])

        assert result == expected

    def test_get_connections(self, t_env):
        result = connections.get_connections(t_env['CCS_PATH'])

        assert type(result) is list

    def test_get_connection_name(self, t_env):
        expected = "Texas Instruments XDS110 USB Debug Probe"
        connxml = os.path.normpath(t_env['CCS_PATH'] +
                                   "/ccs_base/common/targetdb/connections/"
                                   "TIXDS110_Connection.xml")

        result = connections.get_connection_name(connxml)

        assert result == expected
