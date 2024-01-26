from django.db import models


class RankedMonster(models.Model):
    rank = models.IntegerField(null=False, blank=False)
    monster = models.ForeignKey("Game.Monster", on_delete=models.CASCADE, null=False)

    level = models.IntegerField(null=False)
    spells = models.CharField(max_length=255, null=False)
    hit_points = models.IntegerField(null=False)
    action_points = models.IntegerField(null=False)
    movement_points = models.IntegerField(null=False)
    initiative = models.IntegerField(null=False)
    experience_reward = models.IntegerField(null=False)

    neutral_resistance = models.IntegerField(null=False)
    earth_resistance = models.IntegerField(null=False)
    fire_resistance = models.IntegerField(null=False)
    water_resistance = models.IntegerField(null=False)
    air_resistance = models.IntegerField(null=False)
    action_points_dodge = models.IntegerField(null=False)
    movement_points_dodge = models.IntegerField(null=False)

    strenght = models.IntegerField(null=False)
    wisdom = models.IntegerField(null=False)
    inteligence = models.IntegerField(null=False)
    luck = models.IntegerField(null=False)
    agility = models.IntegerField(null=False)

    class Meta:
        constraints = [models.UniqueConstraint("rank", "monster_id", name="unique_rank_for_monster")]
