from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from ... import bootstrap


default_sources = ["roles", "demo"]


class Command(BaseCommand):
    help = "Bootstrap test project with sample user, rules, and content based on selected data file"

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "sources", metavar="source", nargs="*", default=[], help="Data sources."
        )
        group.add_argument(
            "--all",
            "-a",
            action="store_true",
            help="Use all default sources ({})".format(", ".join(default_sources)),
        )

    def get_file_path(self, path, external=False):
        if external:
            candidate = path
        else:
            package_root = Path(__file__).resolve().parents[2]
            candidate = package_root / "builtin_data" / "{file}.json".format(file=path)
        return str(candidate)

    @transaction.atomic
    def handle(self, **options):
        if options["all"]:
            sources = default_sources
        else:
            sources = options["sources"]
        for source in sources:
            for external in (False, True):
                try:
                    with open(self.get_file_path(source, external)) as f:
                        bootstrap(f)
                        break
                except FileNotFoundError:
                    pass
                except Exception as e:
                    raise CommandError(
                        "An error occured while bootstrapping the project. "
                        "Transaction has been rolled back and no data has been stored in the database. "
                        "Use --traceback parameter to display the stacktrace."
                    ) from e
            else:
                raise CommandError(
                    "Could not open specified file ({}). Aborting.".format(source)
                )
