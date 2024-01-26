from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("load_maps")
        call_command("load_doors")
        call_command("load_monsters")
        call_command("load_monster_groups")
