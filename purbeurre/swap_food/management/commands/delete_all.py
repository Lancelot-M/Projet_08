from django.core.management.base import BaseCommand
from swap_food.management.commands.commands import DeleteData


class Command(BaseCommand):

    def handle(self, *args, **options):
        maker = DeleteData()
        maker.clean_all()
        print("DATABASE IS EMPTY")
