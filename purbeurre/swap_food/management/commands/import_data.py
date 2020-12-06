from django.core.management.base import BaseCommand, CommandError
from swap_food.management.commands.commands import ImportData

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('categories', nargs="+", type=int)

    def handle(self, *args, **options):
        maker = ImportData()
        print(maker.make_import(options["categories"][0], options["categories"][1]))