import datetime

from django.core.management import BaseCommand

from ranking.jobs import compile_rankings, get_week_start


class Command(BaseCommand):
    help = "Runs Calculating ranking."

    def add_arguments(self, parser):
        parser.add_argument(
            "--week",
            type=int,
            default=None,
            nargs="?",
            help="Date to calculate ranking for.",
        )

    def handle(self, *args, **options):
        if options["week"] is not None:
            print("Calculating ranking for week", options["week"])
            date: datetime.datetime = get_week_start(options["week"])
        else:
            print("Calculating ranking for current week")
            date: datetime.datetime = datetime.datetime.now()
        compile_rankings(date)
