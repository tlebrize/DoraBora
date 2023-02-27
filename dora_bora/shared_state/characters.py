from collections import defaultdict
from dataclasses import field, dataclass
from .base_state import BaseState


class CharacterNotInMap(BaseException):
    ...


@dataclass
class CharactersState(BaseState):
    maps: dict = field(default_factory=dict)
    cells: defaultdict[dict] = field(default_factory=lambda: defaultdict(dict))

    def move_to_map(self, character, destination):
        if current := self.maps.get(character):
            self.MAPS.characters[current].remove(character)

        self.MAPS.characters[destination].append(character)
        self.maps[character] = destination

    def move_to_cell(self, character, destination):
        if not (map_ := self.maps.get(character)):
            raise CharacterNotInMap(character)

        self.cells[map_][character] = destination

    def get_cell(self, character):
        if not (map_ := self.maps.get(character)):
            raise CharacterNotInMap(character)

        return self.cells[map_].get(character)
