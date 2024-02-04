from django.db import models

from .map import Map


class CharacterQueryset(models.QuerySet):
    async def format_alk(self):
        return "|".join([c.format_alk() async for c in self.all()])

    async def acreate(self, *args, **kwargs):
        if not ("_map" in kwargs or "_map_id" in kwargs):
            map_id, cell_id = Character.get_default_map_id(_class=kwargs.get("_class"))
            kwargs["cell_id"] = cell_id
            kwargs["_map"] = await Map.objects.aget(id=map_id)
        return await super().acreate(*args, **kwargs)

    def create(self, *args, **kwargs):
        if not ("_map" in kwargs or "_map_id" in kwargs):
            map_id, cell_id = Character.get_default_map_id(_class=kwargs.get("_class"))
            kwargs["cell_id"] = cell_id
            kwargs["_map"] = Map.objects.get(id=map_id)
        return super().create(*args, **kwargs)


class Character(models.Model):
    class Gender(models.IntegerChoices):
        MALE = 0
        FEMALE = 1

    class Class(models.IntegerChoices):
        FECA = 1
        OSAMODAS = 2
        ENUTROF = 3
        SRAM = 4
        XELOR = 5
        ECAFLIP = 6
        ENIRIPSA = 7
        IOP = 8
        CRA = 9
        SADIDA = 10
        SACRIEUR = 11
        PANDAWA = 12

    server = models.ForeignKey(
        "Login.Server",
        related_name="characters",
        on_delete=models.CASCADE,
        null=False,
    )
    account = models.ForeignKey(
        "Login.Account",
        related_name="characters",
        on_delete=models.CASCADE,
        null=False,
    )
    _map = models.ForeignKey(
        "Game.Map",
        related_name="characters",
        on_delete=models.SET_NULL,
        null=True,  # nullable in case maps get re-imported. Should never really be null otherwise.
    )
    cell_id = models.IntegerField(null=False, blank=False)

    _class = models.IntegerField(choices=Class, null=False)
    colors = models.JSONField(default=list, null=False)
    energy = models.IntegerField(default=10000, null=False)
    gender = models.IntegerField(choices=Gender, null=False)
    kamas = models.IntegerField(default=0, null=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    spell_points = models.IntegerField(default=0, null=False)
    stat_points = models.IntegerField(default=0, null=False)
    experience = models.IntegerField(default=0, null=False)

    level = models.IntegerField(default=1, null=False)
    current_hit_points = models.IntegerField(default=55, null=False)
    max_hit_points = models.IntegerField(default=55, null=False)
    action_points = models.IntegerField(default=6, null=False)
    movement_points = models.IntegerField(default=3, null=False)
    neutral_resistance = models.IntegerField(default=0, null=False)
    earth_resistance = models.IntegerField(default=0, null=False)
    fire_resistance = models.IntegerField(default=0, null=False)
    water_resistance = models.IntegerField(default=0, null=False)
    air_resistance = models.IntegerField(default=0, null=False)
    action_points_dodge = models.IntegerField(default=0, null=False)
    movement_points_dodge = models.IntegerField(default=0, null=False)
    strength = models.IntegerField(default=0, null=False)
    wisdom = models.IntegerField(default=0, null=False)
    inteligence = models.IntegerField(default=0, null=False)
    luck = models.IntegerField(default=0, null=False)
    agility = models.IntegerField(default=0, null=False)

    objects = CharacterQueryset.as_manager()

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def get_default_map_id(cls, _class):
        # TODO config default map ?
        return {
            cls.Class.FECA: (10300, 323),
            cls.Class.OSAMODAS: (10284, 372),
            cls.Class.ENUTROF: (10299, 271),
            cls.Class.SRAM: (10285, 263),
            cls.Class.XELOR: (10298, 300),
            cls.Class.ECAFLIP: (10276, 296),
            cls.Class.ENIRIPSA: (10283, 299),
            cls.Class.IOP: (10294, 280),
            cls.Class.CRA: (10292, 284),
            cls.Class.SADIDA: (10279, 254),
            cls.Class.SACRIEUR: (10296, 243),
            cls.Class.PANDAWA: (10289, 236),
        }.get(_class, (10298, 314))

    async def teleport(self, map_id, cell_id):
        self._map = await Map.objects.aget(id=map_id)
        self.cell_id = cell_id
        await self.asave()
        return self._map, cell_id

    def get_colors(self):
        return [(hex(c)[2:] if c != -1 else -1) for c in self.colors]

    def get_gfxid(self):
        return f"{self._class}{self.gender}"

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

    def get_basic_gm(self, override_cell_id=None):
        return [
            override_cell_id or self.cell_id,
            1,  # orientation
            0,  # ? level ?
            self.id,
            self.name,
            self._class,  # class,title;
            f"{self.get_gfxid()}^100",  # gfxid^size
            self.gender,
        ]

    def format_gm(self):
        return "GM|+" + ";".join(
            map(
                str,
                [
                    *self.get_basic_gm(),
                    "",  # -1,0,0,0
                    # alignement,?,wings,grade
                    *self.get_colors(),
                    ",,,,",  # equipment
                    "",  # Emote
                    "",  # Emote Timer
                    "",  # Guild Name
                    "",  # Guild Emblem
                    "",  # ?
                    8,  # Speed
                    "",  # Close
                ],
            )
        )

    def format_fight_gm(self, team, cell_id):
        return ";".join(
            map(
                str,
                [
                    *self.get_basic_gm(cell_id),
                    self.level,
                    "0,0,0,0",  # honor ?
                    *self.get_colors(),
                    ",,,,",  # equipment
                    self.current_hit_points,
                    self.action_points,
                    self.movement_points,
                    self.neutral_resistance,
                    self.earth_resistance,
                    self.fire_resistance,
                    self.water_resistance,
                    self.air_resistance,
                    self.action_points_dodge,
                    self.movement_points_dodge,
                    team,
                    "",  # space for mounts
                ],
            )
        )

    def format_gt(self):
        return f"{self.id};{self.name};{self.level}"
