from django.core.management.base import BaseCommand

from ... import bootstrap


class Command(BaseCommand):
    help = "Bootstrap test project with sample user, rules, and content"

    def handle(self, *args, **options):
        bootstrap()
