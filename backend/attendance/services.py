from datetime import datetime, time, timedelta
from typing import Optional

from django.utils import timezone

from account.models import User
from attendance.models import AttendanceStats, Generation, WeeklyStaffInfo
from config.exceptions import NotExistException


def get_current_generation():
    today = timezone.now().date()
    try:
        return Generation.objects.get(start_date__lte=today, end_date__gte=today)
    except Generation.DoesNotExist:
        raise NotExistException("기수 정보가 존재하지 않습니다.")


def get_weeks_since_start(start_date):
    today = timezone.now().date()
    delta = today - start_date
    week = delta.days // 7 + 1
    return week


def get_day_of_week(current_date):
    weekday_number = current_date.weekday()
    days = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
    return days[weekday_number]


def get_attendance_status(request_time: datetime) -> str:
    """
    출석을 요청한 시간을 바탕으로 출결 상태를 반환하는 메서드입니다.
    """

    day_of_week: str = get_day_of_week(request_time.date())
    current_generation: Generation = get_current_generation()

    weekly_staff_info: Optional[WeeklyStaffInfo] = WeeklyStaffInfo.objects.filter(
        generation=current_generation,
        day_of_week=day_of_week,
    ).first()

    if not weekly_staff_info:
        raise NotExistException("주간 운영진 정보가 존재하지 않습니다.")

    start_time: time = weekly_staff_info.start_time
    start_datetime = datetime.combine(request_time.date(), start_time)
    late_datetime = start_datetime + timedelta(minutes=30)

    if request_time > late_datetime:
        return "지각"
    else:
        return "출석"


def check_alternate_attendance(current_user: User) -> bool:
    """
    대체 출석 여부를 판별하기 위한 메서드입니다.
    """

    if int(get_current_generation().name[:-1]) - int(current_user.generation.name[:-1]) > 1:
        return False

    current_time: datetime = timezone.now()
    day_of_week: str = get_day_of_week(current_time.date())
    current_generation: Generation = get_current_generation()

    today_workout_location: str = (
        WeeklyStaffInfo.objects.filter(generation=current_generation, day_of_week=day_of_week)
        .first()
        .workout_location  # type: ignore
    )

    if current_user.workout_location == today_workout_location:
        return False
    else:
        return True


def calculate_attendance_rate(
    attendance_stats: AttendanceStats, current_gen_number: int, user_gen_number: int
) -> float:

    if current_gen_number - user_gen_number < 2:
        late_as_absence = attendance_stats.late // 2
        late_as_attendance = attendance_stats.late % 2

        total_possible_attendance = (
            attendance_stats.attendance + attendance_stats.absence + late_as_attendance + late_as_absence
        )
        effective_attendance = attendance_stats.attendance + late_as_attendance
        if total_possible_attendance > 0:
            attendance_rate = (effective_attendance / total_possible_attendance) * 100
        else:
            attendance_rate = 0.0
    else:
        if attendance_stats.attendance > 0:
            attendance_rate = 100
        else:
            attendance_rate = 0.0

    return attendance_rate
