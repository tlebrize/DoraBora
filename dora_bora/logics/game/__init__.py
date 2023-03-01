from dora_bora.database_accessor import DatabaseAccessor
from dora_bora.logics.base_logic import BaseLogic
from dora_bora.logics.exceptions import NotHandled
from dora_bora.non_blocking_queue import NonBlockingQueue
from dora_bora.shared_state import get_shared_state

from .account import AccountLogic
from .chat import ChatLogic
from .basic import BasicLogic
from .game import GameLogic
from .conquest import ConquestLogic


class RootGameLogic(BaseLogic):
    def __init__(self, server_id):
        super().__init__()
        self.server_id = server_id
        self.shared = get_shared_state()

        self.handlers = {
            "A": AccountLogic(self),
            "c": ChatLogic(self),
            "B": BasicLogic(self),
            "G": GameLogic(self),
            "C": ConquestLogic(self),
        }

    def start(self):
        self.outputs.put("HG")

    def handle_input(self):
        try:
            message = self.inputs.get()
            handler = self.handlers.get(message[0])
            if not handler:
                raise NotHandled(message)
            else:
                handler.handle_input(message[1:])
        except NotHandled as exc:
            print("Not Handled", exc)

    def end(self):
        if getattr(self, "character"):
            if self.shared.clients.remove_character(self.character.id):
                print("Cleanly disconnected.")
            else:
                print("Was already disconnected.")
        else:
            print("Wasn't connected.")
