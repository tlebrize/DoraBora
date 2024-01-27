from django.db import models


class RankedMonsterTemplate(models.Model):
    rank = models.IntegerField(null=False, blank=False)
    monster_template = models.ForeignKey(
        "Game.MonsterTemplate",
        on_delete=models.CASCADE,
        null=False,
        related_name="ranked_monster_templates",
    )

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

    strength = models.IntegerField(null=False)
    wisdom = models.IntegerField(null=False)
    inteligence = models.IntegerField(null=False)
    luck = models.IntegerField(null=False)
    agility = models.IntegerField(null=False)

    class Meta:
        constraints = [models.UniqueConstraint("rank", "monster_template_id", name="unique_rank_for_monster_template")]

    def __str__(self):
        return f"{self.id}: {self.monster_template_id} lvl.{self.level}"
