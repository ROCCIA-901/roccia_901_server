import logging
from datetime import datetime
from typing import Optional

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from account.models import Generation, User
from attendance.models import (
    Attendance,
    AttendanceStats,
    UnavailableDates,
    WeeklyStaffInfo,
)
from attendance.services import get_day_of_week, get_weeks_since_start
from config.celery import app

logger = logging.getLogger("django")


@app.task(name="reject_pending_attendances")
def reject_pending_attendances():
    """
    처리되지 않은 '대기' 상태의 출석 요청을 거절 처리 하는 테스크입니다.
    매일 23시 57분에 실행됩니다.
    """

    today = timezone.now().date()
    if Generation.objects.filter(start_date__lte=today, end_date__gte=today).exists():
        pending_attendances = Attendance.objects.filter(request_processed_status="대기", request_time__date=today)
        pending_attendances.update(request_processed_status="거절")


@app.task(name="holiday_processing")
def holiday_processing():
    """
    휴일 출석을 처리하는 테스크입니다.
    매일 23시 58분에 실행됩니다.
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


@app.task(name="absence_processing")
def absence_processing():
    """
    당일의 출석 내역을 확인하고 결석을 처리하는 테스크입니다.
    매일 23시 59분에 실행됩니다.
    """

    today: datetime = timezone.now().date()
    current_generation_queryset = Generation.objects.filter(start_date__lte=today, end_date__gte=today)
    if current_generation_queryset.exists():

        current_generation: Generation = current_generation_queryset.first()
        start_weekday = current_generation.start_date.weekday()

        expected_run_day = (start_weekday - 1) % 7
        if today.weekday() != expected_run_day:
            return

        week = get_weeks_since_start(current_generation.start_date)

        current_generation_number = int(current_generation.name[:-1])
        previous_generation_name = f"{current_generation_number - 1}기"

        users = User.objects.filter(
            generation__name__in=[previous_generation_name, current_generation.name],
            role="부원",
            is_active=True,
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
                        request_time=today,
                        request_processed_status="승인",
                        attendance_status="결석",
                    )

                    attendance_stats, created = AttendanceStats.objects.get_or_create(
                        user=user,
                        generation=current_generation,
                    )
                    attendance_stats.absence = F("absence") + 1
                    attendance_stats.save()
