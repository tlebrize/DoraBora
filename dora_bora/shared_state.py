from collections import defaultdict

from dora_bora.datamodel import (
    Account,
    Character,
    Server,
    Map,
)


class __SharedState:
    def __init__(self):
        self.characters_at_map = defaultdict(list)
        self.map_of_character = {}

    def move_character(self, character_id, destination_id):
        if current_id := self.map_of_character.get(character_id):
            self.characters_at_map[current_id].remove(character_id)

        self.characters_at_map[destination_id].append(character_id)
        self.map_of_character[character_id] = destination_id


__shared_state_singleton = __SharedState()


def get_shared_state():
    return __shared_state_singleton
