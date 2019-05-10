import os

from tiflash.utils import connections


class TestConnections:
    def test_get_connections_directory(self, tenv):
        expected = os.path.normpath(
            tenv["paths"]["ccs"] + "/ccs_base/common/targetdb/connections"
        )

        result = connections.get_connections_directory(tenv["paths"]["ccs"])

        assert result == expected

    def test_get_connections(self, tenv):
        result = connections.get_connections(tenv["paths"]["ccs"])

        assert type(result) is list

    def test_get_connection_name(self, tenv):
        expected = "Texas Instruments XDS110 USB Debug Probe"
        connxml = os.path.normpath(
            tenv["paths"]["ccs"] + "/ccs_base/common/targetdb/connections/"
            "TIXDS110_Connection.xml"
        )

        result = connections.get_connection_name(connxml)

        assert result == expected
