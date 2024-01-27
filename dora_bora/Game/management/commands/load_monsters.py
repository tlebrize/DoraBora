import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from Game.models import MonsterTemplate, RankedMonsterTemplate


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "monsters.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            monsters = []
            ranks = []

            for row in csv.DictReader(fd, delimiter=",", quotechar='"'):
                ranks_data, monster = MonsterTemplate.from_seed(row)
                monsters.append(monster)
                for data in ranks_data:
                    ranks.append(RankedMonsterTemplate(monster_template_id=monster.id, **data))

                if len(monsters) > 99:
                    print(".", end="")
                    MonsterTemplate.objects.bulk_create(monsters)
                    RankedMonsterTemplate.objects.bulk_create(ranks)
                    monsters = []
                    ranks = []

            if monsters:
                print(".", end="")
                MonsterTemplate.objects.bulk_create(monsters)
                RankedMonsterTemplate.objects.bulk_create(ranks)

        print("\nDone !")
