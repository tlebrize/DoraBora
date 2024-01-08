from django.db import models
import logging

logger = logging.getLogger("django")


class Character(models.Model):
    class GenderChoices(models.IntegerChoices):
        MALE = 0
        FEMALE = 1

    class ClassChoices(models.IntegerChoices):
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
    map = models.ForeignKey(
        "Map.Map",
        related_name="characters",
        on_delete=models.SET_NULL,
        null=True,
    )
    _class = models.IntegerField(choices=ClassChoices, null=False)
    colors = models.JSONField(default=list, null=False)
    energy = models.IntegerField(default=10000, null=False)
    gender = models.IntegerField(choices=GenderChoices, null=False)
    kamas = models.IntegerField(default=0, null=False)
    level = models.IntegerField(default=1, null=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    spell_points = models.IntegerField(default=0, null=False)
    stat_points = models.IntegerField(default=0, null=False)
    experience = models.IntegerField(default=0, null=False)

    def __str__(self):
        return f"{self.name} - ({self.server})"
