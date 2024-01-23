from collections import defaultdict
from django.conf import settings
from django.core.management.base import BaseCommand
from pprint import pprint
import csv

from Game.models import Monster


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_file = settings.BASE_DIR / "Game" / "seeds" / "monsters.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            batch = []

            for row in csv.DictReader(fd, delimiter=",", quotechar='"'):
                batch.append(Monster.from_seed(row))

                if len(batch) > 99:
                    print(".", end="")
                    Monster.objects.bulk_create(batch)
                    batch = []

            if batch:
                print(".", end="")
                Monster.objects.bulk_create(batch)

        print("\nDone !")
