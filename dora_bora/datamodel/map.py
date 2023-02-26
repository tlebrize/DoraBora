from dataclasses import dataclass
from enum import Enum


@dataclass
class Map:
    id: int
    dofus_id: int
    date: str
    width: int
    height: int
    key_: str
    position: [int]

    def format_map_data(self):
        return f"GDM|{self.dofus_id}|{self.date}|{self.key_}"


@dataclass
class MapList:
    maps: [Map]
