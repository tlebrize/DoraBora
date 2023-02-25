from .base import BaseDatabase

from dora_bora.datamodel import Character, CharacterList


class CharactersDatabase(BaseDatabase):
    default_fields = ["id"]
    table = "characters"
    model = Character
    list_model = CharacterList
