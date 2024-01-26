from collections import defaultdict
from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand
from pprint import pprint
import csv

from Game.models import Map, Monster, MonsterGroup, RankedMonster


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            self.load_maps()
            self.load_doors()
            self.load_monsters()
            self.make_monster_groups()
            self.make_monster_groups_relations()

    def load_maps(self):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "maps.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            batch = []
            reader = csv.DictReader(fd, delimiter=",", quotechar="'")
            for row in reader:
                __, _map = Map.from_seed(row)

                batch.append(_map)
                if len(batch) > 99:
                    print(".", end="")
                    Map.objects.bulk_create(batch)
                    batch = []

            if batch:
                print(".", end="")
                Map.objects.bulk_create(batch)

        print("\nDone !")

    def load_doors(self):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "doors.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            batch = defaultdict(dict)

            for row in csv.DictReader(fd, delimiter=",", quotechar="'"):
                batch[int(row.pop("start_map"))][int(row["start_cell"])] = [
                    int(row["target_map"]),
                    int(row["target_cell"]),
                ]

                if len(batch.keys()) > 99:
                    print(".", end="")
                    Map.objects.bulk_set_doors(batch)
                    batch = defaultdict(dict)

            if batch:
                print(".", end="")
                Map.objects.bulk_set_doors(batch)

        print("\nDone !")

    def load_monsters(self):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "monsters.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            monsters = []
            ranks = []

            for row in csv.DictReader(fd, delimiter=",", quotechar='"'):
                ranks_data, monster = Monster.from_seed(row)
                monsters.append(monster)
                for data in ranks_data:
                    ranks.append(RankedMonster(monster_id=monster.id, **data))

                if len(monsters) > 99:
                    print(".", end="")
                    Monster.objects.bulk_create(monsters)
                    RankedMonster.objects.bulk_create(ranks)
                    monsters = []
                    ranks = []

            if monsters:
                print(".", end="")
                Monster.objects.bulk_create(monsters)
                RankedMonster.objects.bulk_create(ranks)

        print("\nDone !")

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
                    MonsterGroup(
                        id=map_id,
                        _map_id=map_id,
                        max_size=max_size,
                        min_size=min_size,
                        size=int(row["numgroup"]),
                        cell_id=None,
                        respawn_delay=None,
                    )
                )

                if len(groups) > 99:
                    print(".", end="")
                    MonsterGroup.objects.bulk_create(groups)
                    groups = []

            if groups:
                print(".", end="")
                MonsterGroup.objects.bulk_create(groups)

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

                ranks_data = {}
                for data in row["monsters"].split("|"):
                    if data:
                        monster_id, level = data.split(",")
                        ranks_data[int(monster_id)] = int(level)

                ranked_queryset = RankedMonster.objects.filter(monster_id__in=ranks_data.keys()).values_list(
                    "id", "level", "monster_id"
                )

                for ranked_id, level, monster_id in ranked_queryset:
                    if ranks_data[monster_id] == level:
                        relations.append(
                            MonsterGroup.monsters.through(
                                rankedmonster_id=ranked_id,
                                monstergroup_id=int(row["id"]),
                            )
                        )

                if len(relations) > 399:
                    print(".", end="")
                    MonsterGroup.monsters.through.objects.bulk_create(relations)
                    relations = []

            if relations:
                print(".", end="")
                MonsterGroup.monsters.through.objects.bulk_create(relations)

        print("\nDone !")
