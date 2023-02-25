from dora_bora.non_blocking_queue import NonBlockingQueue
from dora_bora.database import AccountsDatabase
from dora_bora.datamodel import AccountState

from .exceptions import InvalidAT


class GameLogic:
    def __init__(self, server_id):
        self.server_id = server_id
        self.inputs = NonBlockingQueue()
        self.outputs = NonBlockingQueue()
        self.accounts_db = AccountsDatabase()

    def start(self):
        self.outputs.put("HG")

    def handle_input(self):
        msg = self.inputs.get()
        if not msg.startswith("AT"):
            raise InvalidAT(msg)
        self.account = self.accounts_db.get(int(msg[2:]))

        if self.account.state != AccountState.InLogin:
            raise InvalidAccountState(self.account.state)
        self.accounts_db.set(self.account.id, "state", AccountState.InGame)
