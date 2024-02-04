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
    spells = models.CharField(max_length=255, null=False)

    level = models.IntegerField(null=False)
    hit_points = models.IntegerField(null=False)
    action_points = models.IntegerField(null=False)
    movement_points = models.IntegerField(null=False)
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

    def __str__(self):
        return f"{self.id}:{self.name} lvl.{self.level}"

    @property
    def current_hit_points(self):
        return self.hit_points

    @property
    def max_hit_points(self):
        return self.hit_points

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

    def get_colors(self):
        # TODO for color import for monsters
        return [(hex(int(c))[2:] if c != "-1" else -1) for c in self.colors.split(",")]

    def format_gt(self):
        return f"{self.id};{self.template_id};{self.level}"

    def format_fight_gm(self, team, cell_id):
        return ";".join(
            map(
                str,
                [
                    cell_id,
                    1,
                    0,
                    self.id,
                    self.template_id,  # name?
                    -2,
                    f"{self.gfx_id}^100",  # gfx^size
                    self.rank,
                    *self.get_colors(),
                    "0,0,0,0",  # items
                    self.max_hit_points,
                    self.action_points,
                    self.movement_points,
                    team,
                ],
            )
        )
        # str.append("-2;");
        # str.append(this.mob.getTemplate().getGfxId()).append("^").append(this.mob.getSize()).append(";");
        # str.append(this.mob.getGrade()).append(";");
        # str.append(this.mob.getTemplate().getColors().replace(",", ";")).append(";");
        # //Accessories Mobs (Qu'Tan & Ili) (Change taille démon + ajout item sur mobs en combat)
        # int tst = this.mob.getTemplate().getId();
        # if (tst==534) // Pandawa Ivre
        #     str.append("0,1C3C,1C40,0;");
        # else if (tst==547) // Pandalette ivre
        #     str.append("0,1C3C,1C40,0;");
        # else if (tst==1213)  // Mage Céleste
        #     str.append("0,2BA,847,0;");
        # /*else if (tst==30063) // Yllib - Affiche le Flood derrière la tête
        # {
        #     str.append("0,0,2155,0;");
        # }*/
        # else
        #     str.append("0,0,0,0;");
        # //class fighter
        # str.append(this.getPdvMax()).append(";");
        # str.append(this.mob.getPa()).append(";");
        # str.append(this.mob.getPm()).append(";");
        # str.append(this.team);
