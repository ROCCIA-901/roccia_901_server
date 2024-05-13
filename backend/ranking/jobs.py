from datetime import date, datetime, timedelta

import pytz
from django.db.models import Case, F, FloatField, Sum, Value, When

from config.settings.base import TIME_ZONE
from ranking.models import Ranking
from record.models import BoulderProblem


# Function to get the start and end of the week
# for a given date in Korea Standard Time.
# Example usage:
# monday, sunday = get_week_start_end_kst(datetime.now(pytz.utc))
def get_week_start_end(target_date_utc: datetime = datetime.now(pytz.utc), zone: str = TIME_ZONE) -> tuple[date, date]:
    # Get date in Timezone.
    try:
        timezone = pytz.timezone(zone)
    except pytz.UnknownTimeZoneError:
        raise ValueError("Unknown timezone")
    target_date_in_timezone: datetime = target_date_utc.astimezone(timezone)

    # Calculate the start of the week (Monday).
    start_of_week = target_date_in_timezone - timedelta(days=target_date_in_timezone.weekday())
    # Calculate the end of the week (Sunday).
    end_of_week = start_of_week + timedelta(days=6)

    # Return the start and end of the week
    return start_of_week.date(), end_of_week.date()


def get_week_start(week: int) -> datetime:
    return datetime.fromisocalendar(datetime.now().year, week, 1)


def delete_rankings(generation: int, week: int) -> None:
    Ranking.objects.filter(generation=generation, week=week).delete()


def compile_rankings(target_date_utc: datetime = datetime.now(pytz.utc)) -> tuple:
    # TODO: handle pytz.UnknownTimeZoneError exceptions
    monday, sunday = get_week_start_end(target_date_utc)
    monday_datetime = pytz.timezone(TIME_ZONE).localize(datetime.combine(monday, datetime.min.time()))
    sunday_datetime = pytz.timezone(TIME_ZONE).localize(datetime.combine(sunday, datetime.max.time()))

    # TODO: 성능 개선
    weekly_scores = (
        BoulderProblem.objects.select_related("record__user")
        .filter(record__start_time__range=(monday_datetime, sunday_datetime))
        .annotate(
            score=Case(
                When(workout_level__lt=F("record__user__workout_level"), then=F("count") * Value(0.5)),
                When(workout_level=F("record__user__workout_level"), then=F("count") * Value(1.0)),
                When(workout_level__gt=F("record__user__workout_level"), then=F("count") * Value(2.0)),
                default=Value(0),
                output_field=FloatField(),
            )
        )
        .values("record__user__id")
        .annotate(total_score=Sum("score"))
        .order_by("-total_score")
    )

    year_week_day = tuple(monday_datetime.isocalendar())

    # remove previous rankings for the same week
    delete_rankings(Ranking.CUR_GENERATION, year_week_day[1])
    # add weekly_scores to Ranking model
    objs = [
        Ranking(
            user_id=weekly_score["record__user__id"],
            generation=Ranking.CUR_GENERATION,
            week=year_week_day[1],
            score=weekly_score["total_score"],
        )
        for weekly_score in weekly_scores
    ]
    Ranking.objects.bulk_create(objs)

    return year_week_day
