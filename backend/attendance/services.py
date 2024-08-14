from datetime import datetime, timedelta

from django.utils import timezone

from attendance.models import ActivityDates, WeeklyStaffInfo
from config.exceptions import NotExistException


def get_activity_date():
    today = timezone.now().date()
    try:
        return ActivityDates.objects.get(start_date__lte=today, end_date__gte=today)
    except ActivityDates.DoesNotExist:
        return None


def get_weeks_since_start(start_date):
    today = timezone.now().date()
    delta = today - start_date
    week = delta.days // 7 + 1
    return week


def get_day_of_week(current_date):
    weekday_number = current_date.weekday()
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return days[weekday_number]


def get_attendance_status():
    current_time = timezone.now()
    day_of_week = get_day_of_week(current_time.date())
    activity_date = get_activity_date()
    current_generation = activity_date.generation

    weekly_staff_info = WeeklyStaffInfo.objects.filter(
        generation=current_generation,
        day_of_week=day_of_week,
    ).first()

    if not weekly_staff_info:
        raise NotExistException()

    start_time = weekly_staff_info.start_time
    start_datetime = datetime.combine(current_time.date(), start_time)
    late_datetime = start_datetime + timedelta(minutes=30)

    if current_time > late_datetime:
        return "지각"
    else:
        return "출석"


def check_alternate_attendance(workout_location):
    current_time = timezone.now()
    day_of_week = get_day_of_week(current_time.date())
    activity_date = get_activity_date()
    current_generation = activity_date.generation

    today_workout_location = (
        WeeklyStaffInfo.objects.filter(generation=current_generation, day_of_week=day_of_week).first().workout_location
    )

    if workout_location == today_workout_location:
        return False
    else:
        return True
