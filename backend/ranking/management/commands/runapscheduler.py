import logging
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore

from ranking.jobs import compile_rankings

logger = logging.getLogger(__name__)


@util.close_old_connections
def compile_rankings_job():
    current_date_utc: datetime = datetime.now(pytz.utc)

    (year, week, _) = compile_rankings(current_date_utc)
    print(f"Rankings for the {week}th week of {year} completed.")
    logger.info(f"Rankings for the {week}th week of {year} completed.")

    (year, week, _) = compile_rankings(current_date_utc - timedelta(days=7))
    print(f"Rankings for the {week}th week of {year} completed.")
    logger.info(f"Rankings for the {week}th week of {year} completed.")


class Command(BaseCommand):
    help = "Runs APScheduler."

    def add_arguments(self, parser):
        # interval of scheduler
        parser.add_argument(
            "--days",
            type=int,
            default=0,
            nargs="?",
            help="The --days parameter specifies the interval, in days, between each execution of the scheduler's tasks. This interval determines how frequently the scheduler will run the tasks programmed within the command.",  # noqa
        )
        parser.add_argument(
            "--hours",
            type=int,
            default=0,
            nargs="?",
            help="The --hours parameter specifies the interval, in hours, between each execution of the scheduler's tasks. This interval determines how frequently the scheduler will run the tasks programmed within the command.",  # noqa
        )
        parser.add_argument(
            "--minutes",
            type=int,
            default=0,
            nargs="?",
            help="The --minutes parameter specifies the interval, in minutes, between each execution of the scheduler's tasks. This interval determines how frequently the scheduler will run the tasks programmed within the command.",  # noqa
        )

    def handle(self, *args, **options):
        if options["days"] == 0 and options["hours"] == 0 and options["minutes"] == 0:
            print("Please specify an interval for the scheduler.")
            return

        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            compile_rankings_job,
            trigger=IntervalTrigger(days=options["days"], hours=options["hours"], minutes=options["minutes"]),
            id="compile_rankings",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'compile_rankings_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
