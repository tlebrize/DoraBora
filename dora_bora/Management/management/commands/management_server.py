from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting management."))
        call_command("migrate", no_input=True)
        call_command("runserver", "0.0.0.0:5050")
