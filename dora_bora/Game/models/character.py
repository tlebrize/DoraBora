from django.db import models


class CharacterQueryset(models.QuerySet):
    async def format_alk(self):
        return "|".join([c.format_alk() async for c in self.all()])


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
    # map = models.ForeignKey(
    #     "Map.Map",
    #     related_name="characters",
    #     on_delete=models.SET_NULL,
    #     null=True,
    # )

    _class = models.IntegerField(choices=Class, null=False)
    colors = models.JSONField(default=list, null=False)
    energy = models.IntegerField(default=10000, null=False)
    gender = models.IntegerField(choices=Gender, null=False)
    kamas = models.IntegerField(default=0, null=False)
    level = models.IntegerField(default=1, null=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    spell_points = models.IntegerField(default=0, null=False)
    stat_points = models.IntegerField(default=0, null=False)
    experience = models.IntegerField(default=0, null=False)

    objects = CharacterQueryset.as_manager()

    def __str__(self):
        return f"{self.name} - ({self.server})"

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
