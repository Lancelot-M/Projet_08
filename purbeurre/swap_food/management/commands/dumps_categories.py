from django.core.management.base import BaseCommand
from swap_food.management.commands.commands import DumpsCategories


class Command(BaseCommand):
    def handle(self, *args, **options):
        maker = DumpsCategories()
        maker.make_dump()
