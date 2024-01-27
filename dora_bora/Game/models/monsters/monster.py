from django.db import models


class MonsterQuerySet(models.QuerySet):
    def parse_colors(self):
        return self


class Monster(models.Model):
    template = models.ForeignKey(
        "Game.MonsterTemplate",
        on_delete=models.CASCADE,
        related_name="monsters",
        null=False,
    )
    group = models.ForeignKey(
        "Game.MonsterGroup",
        on_delete=models.CASCADE,
        related_name="monsters",
        null=False,
    )
    _map = models.ForeignKey(
        "Game.Map",
        on_delete=models.CASCADE,
        related_name="monsters",
        null=False,
    )

    name = models.CharField(null=False, blank=False, max_length=127)
    gfx_id = models.IntegerField(null=False, blank=False)
    alignment = models.IntegerField(null=True)
    colors = models.JSONField(default=list, null=False)
    kama_rewards = models.JSONField(default=list, null=False)
    ai_id = models.IntegerField(null=False, blank=False)
    capturable = models.BooleanField(null=False, default=True)
    aggression_range = models.IntegerField(null=True, default=None)

    rank = models.IntegerField(null=False, blank=False)
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

    objects = MonsterQuerySet.as_manager()

    @classmethod
    def from_template(cls, group_id, map_id, rank_template):
        monster_template = rank_template.monster_template
        return cls(
            template_id=monster_template.id,
            group_id=group_id,
            _map_id=map_id,
            # monster
            name=monster_template.name,
            gfx_id=monster_template.gfx_id,
            alignment=monster_template.alignment,
            colors=monster_template.colors,
            kama_rewards=monster_template.kama_rewards,
            ai_id=monster_template.ai_id,
            capturable=monster_template.capturable,
            aggression_range=monster_template.aggression_range,
            # rank
            rank=rank_template.rank,
            level=rank_template.level,
            spells=rank_template.spells,
            hit_points=rank_template.hit_points,
            action_points=rank_template.action_points,
            movement_points=rank_template.movement_points,
            initiative=rank_template.initiative,
            experience_reward=rank_template.experience_reward,
            neutral_resistance=rank_template.neutral_resistance,
            earth_resistance=rank_template.earth_resistance,
            fire_resistance=rank_template.fire_resistance,
            water_resistance=rank_template.water_resistance,
            air_resistance=rank_template.air_resistance,
            action_points_dodge=rank_template.action_points_dodge,
            movement_points_dodge=rank_template.movement_points_dodge,
            strength=rank_template.strength,
            wisdom=rank_template.wisdom,
            inteligence=rank_template.inteligence,
            luck=rank_template.luck,
            agility=rank_template.agility,
        )
