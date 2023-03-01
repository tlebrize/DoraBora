from dataclasses import field, dataclass
from collections import defaultdict
from .base_state import BaseState


@dataclass
class MapsState(BaseState):
    characters: defaultdict[dict] = field(
        default_factory=lambda: defaultdict(list),
    )

    def list_clients_on_map(self, map):
        return [
            self.CLIENTS.characters.get(character)
            for character in self.characters.get(map, [])
        ]
