from dataclasses import field, dataclass
from .base_state import BaseState


@dataclass
class ClientsState(BaseState):
    characters: dict = field(default_factory=dict)

    def register_character(self, character, client):
        if self.characters.get(character):
            replaced = True
        else:
            replaced = False
        self.characters[character] = client
        return replaced

    def remove_character(self, character):
        return bool(self.characters.pop(character, False))
