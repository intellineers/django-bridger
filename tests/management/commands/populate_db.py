from django.core.management.base import BaseCommand, CommandError

from tests.factories import ModelTestFactory


class Command(BaseCommand):
    help = "Populate the Database with Data"

    def handle(self, *args, **options):
        ModelTestFactory.create_batch(50)
