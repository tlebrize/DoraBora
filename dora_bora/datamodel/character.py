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
    xp: int


@dataclass
class CharacterList:
    characters: [Character]


"""
`id`,
`name`,
`sexe`,
`class`,
`color1`,
`color2`,
`color3`,
`kamas`,
`spellboost`,
`capital`,
`energy`,
`level`,
`xp`,
`size`,
`gfx`,
`account`,
`cell`,
`map`,
`spells`,
`objets`,
`storeObjets`,
`morphMode`,
`server`
"""
