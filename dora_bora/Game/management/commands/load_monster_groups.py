import csv
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand

from Game.models import MonsterGroupTemplate, RankedMonsterTemplate


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.make_monster_groups()
        self.make_monster_groups_relations()

    def make_monster_groups(self):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "maps.csv"
        print("Creating monster groups")

        groups = []
        with open(seed_file, newline="") as fd:
            for row in csv.DictReader(fd, delimiter=",", quotechar="'"):
                monsters_data = row["monsters"]
                if not monsters_data:
                    continue

                map_id = row["id"]
                if row["fixSize"] != "-1":
                    max_size, min_size = int(row["fixSize"]), int(row["fixSize"])
                else:
                    max_size, min_size = int(row["maxSize"]), int(row["minSize"])
                groups.append(
                    MonsterGroupTemplate(
                        id=map_id,
                        _map_id=map_id,
                        max_size=max_size,
                        min_size=min_size,
                        cell_id=None,
                        respawn_delay=None,
                    )
                )

                if len(groups) > 99:
                    print(".", end="")
                    MonsterGroupTemplate.objects.bulk_create(groups)
                    groups = []

            if groups:
                print(".", end="")
                MonsterGroupTemplate.objects.bulk_create(groups)

            print("\nDone !")

    def make_monster_groups_relations(self):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "maps.csv"
        print("Adding monsters to groups")

        relations = []
        with open(seed_file, newline="") as fd:
            for row in csv.DictReader(fd, delimiter=",", quotechar="'"):
                monsters_data = row["monsters"]
                if not monsters_data:
                    continue

                ranks_data = defaultdict(list)
                for data in row["monsters"].split("|"):
                    if data:
                        monster_id, level = data.split(",")
                        ranks_data[int(monster_id)].append(int(level))

                ranked_queryset = RankedMonsterTemplate.objects.filter(
                    monster_template_id__in=ranks_data.keys()
                ).values_list("id", "level", "monster_template_id")

                for ranked_id, level, monster_id in ranked_queryset:
                    if level in ranks_data[monster_id]:
                        relations.append(
                            MonsterGroupTemplate.monster_templates.through(
                                rankedmonstertemplate_id=ranked_id,
                                monstergrouptemplate_id=int(row["id"]),
                            )
                        )

                if len(relations) > 399:
                    print(".", end="")
                    MonsterGroupTemplate.monster_templates.through.objects.bulk_create(relations)
                    relations = []

            if relations:
                print(".", end="")
                MonsterGroupTemplate.monster_templates.through.objects.bulk_create(relations)

        print("\nDone !")
