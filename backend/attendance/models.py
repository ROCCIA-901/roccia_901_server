from django.db import models

from account.models import Generation, User
from common.choices import WORKOUT_LOCATION_CHOICES


class Attendance(models.Model):
    REQUEST_STATUS_CHOICES: tuple[tuple[str, str], ...] = (
        ("승인", "승인"),
        ("거절", "거절"),
        ("대기", "대기"),
    )

    ATTENDANCE_STATUS_CHOICES: tuple[tuple[str, str], ...] = (
        ("출석", "출석"),
        ("지각", "지각"),
        ("결석", "결석"),
        ("휴일", "휴일"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances")  # type: ignore
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="attendance", help_text="기수"
    )  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, null=True, help_text="운동 지점"
    )  # type: ignore
    week = models.IntegerField(null=True, help_text="주차")  # type: ignore
    request_time = models.DateTimeField(null=True, help_text="출석 요청 시간")  # type: ignore
    request_processed_status = models.CharField(
        max_length=20, choices=REQUEST_STATUS_CHOICES, default="대기", null=True, help_text="요청 상태"
    )  # type: ignore
    request_processed_time = models.DateTimeField(null=True, help_text="요청 처리 시간")  # type: ignore
    request_processed_user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="processed_requests", help_text="요청을 처리한 사용자"
    )  # type: ignore
    attendance_status = models.CharField(
        max_length=20, choices=ATTENDANCE_STATUS_CHOICES, null=True, help_text="출석 상태"
    )  # type: ignore
    is_alternate = models.BooleanField(default=False, help_text="대체 출석 여부")  # type: ignore

    class Meta:
        db_table = "attendance"
        ordering = ["-request_time"]


class AttendanceStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance_stats")  # type: ignore
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="attendance_stats", help_text="기수"
    )  # type: ignore
    attendance = models.IntegerField(default=0, help_text="출석 횟수")  # type: ignore
    late = models.IntegerField(default=0, help_text="지각 횟수")  # type: ignore
    absence = models.IntegerField(default=0, help_text="결석 횟수")  # type: ignore

    class Meta:
        db_table = "attendance_stats"


class UnavailableDates(models.Model):
    date = models.DateField(help_text="휴일")  # type: ignore

    class Meta:
        db_table = "unavailable_dates"


class WeeklyStaffInfo(models.Model):
    DAY_OF_WEEK_CHOICES: tuple[tuple[str, str], ...] = (
        ("월요일", "월요일"),
        ("화요일", "화요일"),
        ("수요일", "수요일"),
        ("목요일", "목요일"),
        ("금요일", "금요일"),
    )

    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="weekly_staff_info", help_text="기수"
    )  # type: ignore
    staff = models.ForeignKey(User, on_delete=models.CASCADE, help_text="운영진")  # type: ignore
    day_of_week = models.CharField(max_length=10, choices=DAY_OF_WEEK_CHOICES, help_text="요일")  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, null=True, help_text="운동 지점"
    )  # type: ignore
    start_time = models.TimeField(help_text="운동 시작 시간")  # type: ignore

    class Meta:
        db_table = "weekly_staff_info"
