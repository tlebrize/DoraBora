from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting management."))
        call_command("migrate", no_input=True)
        call_command("runserver", "0.0.0.0:5050")
