from .base import BaseDatabase
from dora_bora.datamodel import Map, MapList


class MapsDatabase(BaseDatabase):
    table = "maps"
    model = Map
    list_model = MapList
