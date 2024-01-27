from django.db import models

from DoraBora.utils import get_model

Monster = get_model("Game.Monster")


class MonsterGroupQuerySet(models.QuerySet):
    def create_from_template(self, group_template):
        group = self.create(
            template_id=group_template.id,
            _map_id=group_template._map_id,
            cell_id=group_template._map.get_random_walkable_cell_id(),
        )

        Monster.objects.bulk_create(
            [
                Monster.from_template(
                    group_id=group.id,
                    map_id=group_template._map_id,
                    rank_template=rank_template,
                )
                for rank_template in group_template.monster_templates.all()
            ]
        )

    def format_GM(self):
        return "|".join([group.format_GM() for group in self.all()])


class MonsterGroup(models.Model):
    template = models.ForeignKey(
        "Game.MonsterGroupTemplate",
        on_delete=models.CASCADE,
        related_name="monster_groups",
        null=False,
    )

    cell_id = models.IntegerField(null=False)
    _map = models.ForeignKey(
        "Game.Map",
        on_delete=models.CASCADE,
        related_name="monster_groups",
        null=False,
    )

    objects = MonsterGroupQuerySet.as_manager()

    @property
    def orientation(self):
        return 0

    @property
    def star_bonus(self):
        return 0

    def format_GM(self):
        monsters_ids = self.monsters.values_list("template_id", flat=True)
        monsters_gfxs = self.monsters.values_list("gfx_id", flat=True)
        monsters_levels = self.monsters.values_list("level", flat=True)
        monsters_colors = self.monsters.values_list("colors", flat=True)
        return "+" + ";".join(
            map(
                str,
                [
                    self.cell_id,
                    self.orientation,
                    self.star_bonus,
                    self.id,
                    ",".join(map(str, monsters_ids)),
                    -3,
                    ",".join(map(lambda g: f"{g}^100", monsters_gfxs)),
                    ",".join(map(str, monsters_levels)),
                    ",".join(map(lambda c: f"{c};0,0,0,0;", monsters_colors)),
                ],
            )
        )
