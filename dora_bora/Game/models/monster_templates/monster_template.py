from django.db import models


class MonsterTemplate(models.Model):
    name = models.CharField(null=False, blank=False, max_length=127)
    gfx_id = models.IntegerField(null=False, blank=False)
    alignment = models.IntegerField(null=True)
    colors = models.JSONField(default=list, null=False)
    kama_rewards = models.JSONField(default=list, null=False)
    ai_id = models.IntegerField(null=False, blank=False)
    capturable = models.BooleanField(null=False, default=True)
    aggression_range = models.IntegerField(null=True, default=None)

    def __str__(self):
        return self.name

    @classmethod
    def from_seed(cls, row):
        if row["align"] != -1:
            alignment = row["align"]
        else:
            alignment = None

        basics = row["grades"].split("|")
        stats = row["stats"].split("|")
        spells = row["spells"].split("|")
        pdvs = row["pdvs"].split("|")
        points = row["points"].split("|")
        initiatives = row["inits"].split("|")
        exps = row["exps"].split("|")

        ranks = []

        zipped = zip(range(12), basics, stats, spells, pdvs, points, initiatives, exps)
        for rank, basics, raw_stats, spells, hit_points, points, initiative, experience_reward in zipped:
            if basics == "1@":
                continue
            level, resists_raw = basics.split("@")
            resists = resists_raw.split(";")
            strength, wisdom, inteligence, luck, agility = raw_stats.split(",")
            action_points, movement_points = points.split(";")

            ranks.append(
                {
                    "rank": int(rank),
                    "level": int(level),
                    "neutral_resistance": int(resists[0]),
                    "earth_resistance": int(resists[1]),
                    "fire_resistance": int(resists[2]),
                    "water_resistance": int(resists[3]),
                    "air_resistance": int(resists[4]),
                    "action_points_dodge": int(resists[5]),
                    "movement_points_dodge": int(resists[6]),
                    "strength": int(strength),
                    "wisdom": int(wisdom),
                    "inteligence": int(inteligence),
                    "luck": int(luck),
                    "agility": int(agility),
                    "spells": spells,  # TODO relational
                    "hit_points": int(hit_points),
                    "action_points": int(action_points),
                    "movement_points": int(movement_points),
                    "initiative": int(initiative),
                    "experience_reward": int(experience_reward),
                }
            )

        if row["aggroDistance"] == "0":
            aggression_range = None
        else:
            aggression_range = int(row["aggroDistance"])

        kama_rewards = [int(row["minKamas"]), int(row["maxKamas"])]

        return ranks, cls(
            id=int(row["id"]),
            name=row["name"],
            gfx_id=int(row["gfxID"]),
            alignment=alignment,
            colors=row["colors"],
            kama_rewards=kama_rewards,
            ai_id=row["AI_Type"],
            capturable=bool(int(row["capturable"])),
            aggression_range=aggression_range,
        )