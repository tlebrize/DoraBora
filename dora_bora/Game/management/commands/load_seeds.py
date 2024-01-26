from collections import defaultdict
from django.db import transaction
from django.conf import settings
from django.core.management.base import BaseCommand
from pprint import pprint
import csv

from Game.models import Map, Monster, MonsterGroup, RankedMonster


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.groups_datas = {}  # TODO Those are really heavy, maybe there's a better way ?
        self.ranked_monsters_on_map = defaultdict(list)
        self.monsters_on_maps = defaultdict(list)

        with transaction.atomic():
            self.load_maps()
            self.load_doors()
            self.load_monsters()
            self.make_monster_groups()

    def load_maps(self):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "maps.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            batch = []
            reader = csv.DictReader(fd, delimiter=",", quotechar="'")
            for row in reader:
                group_data, _map = Map.from_seed(row)
                if group_data[_map.id]["monsters"]:
                    self.groups_datas.update(group_data)
                    for monster_id, rank in group_data[_map.id]["monsters"]:
                        self.monsters_on_maps[monster_id].append(_map.id)

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
                    for ranked_monster in RankedMonster.objects.bulk_create(ranks):
                        map_id = self.monsters_on_maps.get(ranked_monster.monster_id)
                        if map_id:
                            self.ranked_monsters_on_map[map_id].append(ranked_monster.id)
                    monsters = []
                    ranks = []

            if monsters:
                print(".", end="")
                Monster.objects.bulk_create(monsters)
                for ranked_monster in RankedMonster.objects.bulk_create(ranks):
                    map_id = self.monsters_on_maps[ranked_monster.monster_id]
                    self.ranked_monsters_on_map[map_id].append(ranked_monster.id)

        print("\nDone !")

    def make_monster_groups(self):
        print("Creating monster groups on maps")

        groups = []
        for map_id, group_data in self.groups_datas.items():
            groups.append(MonsterGroup.from_seed(map_id, group_data))

            if len(groups) > 99:
                print(".", end="")
                MonsterGroup.objects.bulk_create(groups)
                groups = []

        if groups:
            print(".", end="")
            MonsterGroup.objects.bulk_create(groups)
            groups = []

        relations = []
        for map_id, group_id in MonsterGroup.objects.values_list("_map_id", "id"):
            for ranked_monster_id in self.ranked_monsters_on_map.get(map_id, []):
                relations.append(
                    MonsterGroup.monsters.through(
                        monster_group_id=group_id,
                        rankedmonster_id=ranked_monster_id,
                    )
                )

            if len(relations) > 99:
                print(".", end="")
                MonsterGroup.monsters.through.bulk_create(relations)
                relations = []

        if relations:
            print(".", end="")
            MonsterGroup.monsters.through.bulk_create(relations)
            relations = []

        print("\nDone !")
