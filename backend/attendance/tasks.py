import logging
from datetime import datetime, timedelta
from typing import Optional

from django.db import transaction
from django.utils import timezone

from account.models import Generation, User
from attendance.models import Attendance, UnavailableDates, WeeklyStaffInfo
from attendance.services import get_day_of_week, get_weeks_since_start
from config.celery import app

logger = logging.getLogger("django")


@app.task(name="reject_pending_attendances")
def reject_pending_attendances():
    """
    처리되지 않은 '대기' 상태의 출석 요청을 거절 처리 하는 테스크입니다.
    """

    current_date = timezone.now().date()
    yesterday = current_date - timedelta(days=1)
    if Generation.objects.filter(start_date__lte=yesterday, end_date__gte=yesterday).exists():
        pending_attendances = Attendance.objects.filter(request_processed_status="대기", request_time__date=yesterday)
        pending_attendances.update(request_processed_status="거절")


@app.task(name="holiday_processing")
def holiday_processing():
    """
    휴일 출석을 처리하는 테스크입니다.
    """

    current_date: datetime = timezone.now().date()
    current_generation_queryset = Generation.objects.filter(start_date__lte=current_date, end_date__gte=current_date)
    if current_generation_queryset.exists() and UnavailableDates.objects.filter(date=current_date).exists():

        day_of_week: str = get_day_of_week(current_date)
        current_generation: Generation = current_generation_queryset.first()

        weekly_staff_info: Optional[WeeklyStaffInfo] = WeeklyStaffInfo.objects.filter(
            generation=current_generation, day_of_week=day_of_week
        ).first()

        if weekly_staff_info is None:
            return

        current_generation_name = current_generation.name
        current_generation_number = int(current_generation_name[:-1])
        previous_generation_name = f"{current_generation_number - 1}기"

        week: int = get_weeks_since_start(current_generation.start_date)

        users = User.objects.filter(
            workout_location=weekly_staff_info.workout_location,
            generation__name__in=[previous_generation_name, current_generation_name],
        )

        with transaction.atomic():
            for user in users:
                if not Attendance.objects.filter(
                    user=user,
                    generation=current_generation,
                    week=week,
                    request_processed_status="승인",
                ).exists():
                    Attendance.objects.create(
                        user=user,
                        generation=current_generation,
                        week=week,
                        request_time=current_date,
                        request_processed_status="승인",
                        attendance_status="휴일",
                    )
