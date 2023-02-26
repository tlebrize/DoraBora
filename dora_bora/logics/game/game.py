from dora_bora.non_blocking_queue import NonBlockingQueue
from dora_bora.database_accessor import DatabaseAccessor
from dora_bora.datamodel import AccountState, Gender, Class

from .account import AccountLogic


class GameLogic:
    def __init__(self, server_id):
        self.server_id = server_id
        self.inputs = NonBlockingQueue()
        self.outputs = NonBlockingQueue()
        self.db = DatabaseAccessor()
        self.account_logic = AccountLogic(self)

    def start(self):
        self.outputs.put("HG")

    def handle_input(self):
        message = self.inputs.get()
        if message.startswith("A"):
            self.account_logic.handle_input(message[1:])
        elif message.startswith("G"):
            self.handle_game_input(message[1:])

    def handle_game_input(self, message):
        if message.startswith("C"):
            self.send_game_create(message[1:])

    def send_game_create(self, data):
        self.outputs.put(f"GCK|1|{self.character.name}")
        # send stats ?
