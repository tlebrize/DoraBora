from dataclasses import dataclass
from enum import Enum


class Gender(int, Enum):
    Male = 0
    Female = 1


class Class(int, Enum):
    Feca = 1
    Osamodas = 2
    Enutrof = 3
    Sram = 4
    Xelor = 5
    Ecaflip = 6
    Eniripsa = 7
    Iop = 8
    Cra = 9
    Sadida = 10
    Sacrieur = 11
    Pandawa = 12


@dataclass
class Character:
    account_id: int
    map_id: int
    class_: Class
    colors: [int]
    energy: int
    gender: Gender
    id: int
    kamas: int
    level: int
    name: str
    server_id: int
    spell_points: int
    stat_points: int
    experience: int

    def get_colors(self):
        return [(hex(c)[2:] if c != -1 else -1) for c in self.colors]

    def get_gfxid(self):
        return self.class_ * 10 + self.gender

    def format_alk(self):
        return ";".join(
            map(
                str,
                [
                    self.id,
                    self.name,
                    self.level,
                    self.get_gfxid(),
                    *self.get_colors(),
                    ",,,,",  # items (getGMStuffString ?)
                    0,  # seller mode
                    self.server_id,
                    0,  # is dead ?
                ],
            )
        )

    def format_pods(self):
        return "Ow0|999"  # `Ow`used_pods|max_pods


@dataclass
class CharacterList:
    characters: [Character]

    def format_alk(self):
        return "|".join([c.format_alk() for c in self.characters])

    def count(self):
        return len(self.characters)
