from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ... import bootstrap


class Command(BaseCommand):
    help = "Bootstrap test project with sample user, rules, and content based on selected data file"

    def add_arguments(self, parser):
        parser.add_argument("file")
        parser.add_argument(
            "--external",
            "-e",
            action="store_true",
            dest="external",
            help="Treats provided name as path to external data source, instead of using one of the builtin files",
        )

    def get_file_path(self, path, external):
        if external:
            candidate = path
        else:
            package_root = Path(__file__).resolve().parents[2]
            candidate = package_root / "builtin_data" / "{file}.json".format(file=path)
        return candidate

    def handle(self, *args, **options):
        candidate = self.get_file_path(options["file"], options["external"])
        try:
            with open(candidate) as f, transaction.atomic():
                bootstrap(f)
        except FileNotFoundError as e:
            raise CommandError(
                "Could not open specified file ({}). Aborting.".format(candidate)
            )
        except Exception as e:
            raise CommandError(
                "An error occured while bootstrapping the project. "
                "Transaction has been rolled back and no data has been stored in the database. "
                "Use --traceback parameter to display the stacktrace."
            ) from e
