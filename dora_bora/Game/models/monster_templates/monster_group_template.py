from django.db import models


class MonsterGroupTemplate(models.Model):
    _map = models.OneToOneField(
        "Game.Map",
        null=False,
        related_name="monster_group_template",
        on_delete=models.CASCADE,
    )
    monster_templates = models.ManyToManyField(
        "Game.RankedMonsterTemplate",
        related_name="monster_group_templates",
    )
    max_size = models.IntegerField(null=False)
    min_size = models.IntegerField(null=False)

    cell_id = models.IntegerField(null=True, blank=False, default=None)
    respawn_delay = models.IntegerField(null=True, blank=False, default=None)
