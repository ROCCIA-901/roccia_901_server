from django.utils import timezone

from attendance.models import ActivityDates


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
