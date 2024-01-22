from collections import defaultdict
from django.conf import settings
from django.core.management.base import BaseCommand
from pprint import pprint
import csv

from Game.models import Map


class Command(BaseCommand):
    def handle(self, *args, **options):
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
