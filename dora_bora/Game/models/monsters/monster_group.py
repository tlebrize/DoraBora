from django.db import models


class MonsterGroup(models.Model):
    _map = models.OneToOneField(
        "Game.Map",
        null=False,
        related_name="monster_group",
        on_delete=models.CASCADE,
    )
    monsters = models.ManyToManyField("Game.RankedMonster")
    max_size = models.IntegerField(null=False)
    min_size = models.IntegerField(null=False)
    size = models.IntegerField(null=False)

    cell_id = models.IntegerField(null=True, blank=False, default=None)
    respawn_delay = models.IntegerField(null=True, blank=False, default=None)
