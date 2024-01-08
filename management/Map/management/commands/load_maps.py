from django.conf import settings
from django.core.management.base import BaseCommand
from pprint import pprint
import csv

from Map.models import Map


class Command(BaseCommand):
    def handle(self, *args, **options):
        seed_file = settings.BASE_DIR / "Map" / "seeds" / "maps.csv"
        print("Importing", seed_file)
        with open(seed_file, newline="") as fd:
            batch = []
            reader = csv.DictReader(fd, delimiter=",", quotechar="'")
            for row in reader:
                batch.append(Map.from_seed(row))
                if len(batch) > 99:
                    print(".", end="")
                    Map.objects.bulk_create(batch)
                    batch = []

            if batch:
                print(".", end="")
                Map.objects.bulk_create(batch)

        print("\nDone !")
