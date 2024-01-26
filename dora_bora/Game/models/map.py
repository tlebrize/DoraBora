import random
from django.db import models

from Game.ank_crypto import ank_is_map_crypted, ank_decrypt_raw_map_data
from Game.ank_encodings import ank_decode_map_data
from DoraBora.utils import get_model

MonsterGroupTemplate = get_model("Game.MonsterGroupTemplate")
MonsterGroup = get_model("Game.MonsterGroup")


class MapQuerySet(models.QuerySet):
    def bulk_set_doors(self, batch):
        map_ids = list(batch.keys())
        maps_queryset = self.filter(id__in=map_ids)
        maps_objects = [map.set_doors(batch.get(map.id)) for map in maps_queryset]
        self.bulk_update(maps_objects, ["doors"])


class Map(models.Model):
    capabilities = models.IntegerField(null=False, blank=False)
    date = models.CharField(max_length=255, null=False, blank=False)
    forbidden = models.JSONField(default=list, null=False, blank=False)
    height = models.IntegerField(null=False, blank=False)
    key = models.TextField(null=True, blank=True)
    raw_map_data = models.TextField(null=False, blank=False)
    map_data = models.JSONField(null=True, blank=True)
    places = models.JSONField(default=list, null=False, blank=True)
    position = models.JSONField(default=list, null=False, blank=False)
    sniffed = models.IntegerField(null=False, blank=False)
    width = models.IntegerField(null=False, blank=False)
    doors = models.JSONField(default=dict, null=False, blank=True)
    max_group_count = models.IntegerField(null=False)

    objects = MapQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.position['x']},{self.position['y']},{self.position['z']}"

    def format_GDM(self):
        return f"GDM|{self.id}|{self.date}|{self.key}"

    def format_GDF(self):
        if self.map_data:  #           interactive;state
            return "".join([f'|{cell["cell_id"]};1;1' for cell in self.map_data if cell.get("obj")])
        else:
            return ""

    def set_doors(self, doors):
        self.doors.update(doors)
        return self

    @classmethod
    def from_seed(cls, row):
        forbidden_parsed = dict(
            zip(
                ["shop", "perceptor", "prism", "teleport", "duel", "aggression", "canal"],
                map(bool, map(int, row["forbidden"].split(";") + [0, 0, 0, 0, 0, 0, 0])),
            )
        )

        x, y, z = row["mappos"].split(",")
        position_parsed = {"x": int(x), "y": int(y), "z": int(z)}

        if ank_is_map_crypted(row["mapData"]):
            # encoded_map_data = ank_decrypt_raw_map_data(row["mapData"], row["key"])
            # map_data = ank_decode_map_data(encoded_map_data)
            map_data = None
        else:
            map_data = ank_decode_map_data(row["mapData"])

        group_data = {
            "max_size": int(row["maxSize"]),
            "min_size": int(row["minSize"]),
            "monsters": [list(map(int, m.split(","))) for m in filter(None, row["monsters"].split("|"))],
        }

        id_ = int(row["id"])

        return cls(
            id=id_,
            position=position_parsed,
            forbidden=forbidden_parsed,
            height=int(row["height"]),
            width=int(row["width"]),
            sniffed=int(row["sniffed"]),
            date=row["date"],
            capabilities=int(row["capabilities"]),
            places=list(filter(None, row["places"].split("|"))),
            raw_map_data=row["mapData"],
            key=row["key"],
            map_data=map_data,
            max_group_count=int(row["numgroup"]),
        )

    def format_monster_groups_GM(self):
        if hasattr(self, "monster_group_template"):
            self.spawn_monster_groups()
            return self.monster_groups.format_GM()

    def get_random_walkable_cell_id(self):
        walkable = []
        for cell in self.map_data:
            if cell["walkable"]:
                walkable.append(cell["cell_id"])
        if walkable:
            return random.choice(walkable)
        else:
            return None

    def spawn_monster_groups(self):
        difference = self.max_group_count - self.monster_groups.count()
        if difference > 0:
            for _ in range(difference):
                MonsterGroup.objects.create_from_template(self.monster_group_template)
