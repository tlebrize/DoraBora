from .base import BaseDatabase

from dora_bora.datamodel import Server, ServerList


class ServersDatabase(BaseDatabase):
    default_fields = ["id", "state"]
    table = "servers"
    model = Server
    list_model = ServerList

    def count_characters(self, account_id):
        return self.execute(
            """
SELECT s.id, count(c.id)
FROM servers s
    JOIN characters c ON c.server_id = s.id
WHERE c.account_id = %s
GROUP BY s.id;
            """,
            [account_id],
        )
