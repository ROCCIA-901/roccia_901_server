from datetime import date, datetime, timedelta
from typing import Any, Union

import pytz
from django.db.models import Case, F, FloatField, Sum, Value, When

from ranking.models import Ranking
from record.models import BoulderProblem


# Function to get the start and end of the week
# for a given date in Korea Standard Time.
# Example usage:
# monday, sunday = get_week_start_end_kst(datetime.now(pytz.utc))
def get_week_start_end(
    current_date_utc: datetime = datetime.now(pytz.utc), zone: str = "Asia/Seoul"
) -> tuple[date, date]:
    # Get date in Timezone.
    try:
        timezone = pytz.timezone(zone)
    except pytz.UnknownTimeZoneError:
        raise ValueError("Unknown timezone")
    current_date_in_timezone: datetime = current_date_utc.astimezone(timezone)

    # Calculate the start of the week (Monday).
    start_of_week = current_date_in_timezone - timedelta(days=current_date_in_timezone.weekday())
    # Calculate the end of the week (Sunday).
    end_of_week = start_of_week + timedelta(days=6)

    # Return the start and end of the week
    return start_of_week.date(), end_of_week.date()


def find_choice_index(choice_value: Any, model_field_choices: tuple[Any]) -> Union[int, None]:
    for index, (value, _) in enumerate(model_field_choices):
        if value == choice_value:
            return index
    return None


def compile_rankings(current_date_utc: datetime = datetime.now(pytz.utc)):
    # TODO: handle exceptions
    # TODO: handle timezone
    monday, sunday = get_week_start_end(current_date_utc)
    monday_datetime = pytz.timezone("Asia/Seoul").localize(datetime.combine(monday, datetime.min.time()))
    sunday_datetime = pytz.timezone("Asia/Seoul").localize(datetime.combine(sunday, datetime.max.time()))

    # TODO: 성능 개선
    weekly_scores = (
        BoulderProblem.objects.select_related("record__user")
        .filter(record__start_time__range=(monday_datetime, sunday_datetime))
        .values("record__start_time", "record__user__workout_level")
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

    # add weekly_scores to Ranking model
    objs = [
        Ranking(
            user_id=weekly_score["record__user__id"],
            generation=Ranking.CUR_GENERATION,
            week=current_date_utc.isocalendar()[1],
            score=weekly_score["total_score"],
        )
        for weekly_score in weekly_scores
    ]
    Ranking.objects.bulk_create(objs)
