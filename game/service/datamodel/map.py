from dataclasses import dataclass
from enum import Enum


@dataclass
class Map:
    id: int
    dofus_id: int
    date: str
    width: int
    height: int
    key: str
    position: [int]
    capabilities: int
    fix_size: int
    forbidden: dict
    group_count: int
    raw_map_data: str
    map_data: dict
    max_size: int
    min_size: int
    monsters: dict
    places: dict
    sniffed: int

    def format_map_data(self):
        return f"GDM|{self.dofus_id}|{self.date}|{self.key}"


@dataclass
class MapList:
    maps: [Map]
