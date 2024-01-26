from django.db import models

from Game.ank_crypto import ank_is_map_crypted, ank_decrypt_raw_map_data
from Game.ank_encodings import ank_decode_map_data


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

    objects = MapQuerySet.as_manager()

    def __str__(self):
        return f"{self.id} - {self.position['x']},{self.position['y']},{self.position['z']}"

    def format_GDM(self):
        return f"GDM|{self.id}|{self.date}|{self.key}"

    def format_GDF(self):
        if self.map_data:  #           interactive;state
            return "GDF" + "".join([f'|{cell["cell_id"]};1;1' for cell in self.map_data if cell.get("obj")])
        else:
            return ""

    def set_doors(self, doors):
        self.doors.update(doors)
        return self

    @classmethod
    def from_seed(cls, row):
        """
        'capabilities': '15',
        'date': '0903300949',
        'fixSize': '-1',
        'forbidden': '0;0;0;0;0;0;0',
        'height': '17',
        'id': '1558',
        'key': '625969222E43292A7D6B633C60492D23562149777B51492D7B4271223E35756263337950393C5428694546285D5F7C3A72636B2F43375F4658397A617772263623596E4F6D7E3E2C772A7046312E5339416977743C542532355C4B3E713F2F7C5F2627454C4621375F3D25326249792F32597F3061517D695954596425326220713E6B3F7E2D5D2927514F552E7952402532355057212D46772F5B404F6B3A715642447D69384C455B472C3847296A4877315E344A6D2D51746A5C4A5D792E4F7F454446676261',
        'mapData': '...',
        'mappos': '0,3,20',
        'maxSize': '6',
        'minSize': '1',
        'monsters': '',
        'numgroup': '3',
        'places': 'e6fifjfwfxfKfLfZ|drdFdGdTdUd7d8ek',
        'sniffed': '0',
        'width': '15'
        """

        forbidden_parsed = dict(
            zip(
                [
                    "shop",
                    "perceptor",
                    "prism",
                    "teleport",
                    "duel",
                    "aggression",
                    "canal",
                ],
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

        return {id_: group_data}, cls(
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
        )
