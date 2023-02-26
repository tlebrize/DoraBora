from .base import BaseDatabase

from dora_bora.datamodel import Server, ServerList


class ServersDatabase(BaseDatabase):
    table = "servers"
    model = Server
    list_model = ServerList

    def count_characters(self, account_id):
        counts = self.execute(
            """
SELECT s.id, count(c.id)
FROM servers s
    JOIN characters c ON c.server_id = s.id
WHERE c.account_id = %s
GROUP BY s.id;
            """,
            [account_id],
        )
        return [(c["id"], c["count"]) for c in counts]
