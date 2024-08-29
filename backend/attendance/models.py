# mypy: ignore-errors

from django.db import models

from account.models import Generation, User
from common.choices import WORKOUT_LOCATION_CHOICES


class Attendance(models.Model):
    REQUEST_STATUS_CHOICES = (
        ("승인", "승인"),
        ("거절", "거절"),
        ("대기", "대기"),
    )

    ATTENDANCE_STATUS_CHOICES = (
        ("출석", "출석"),
        ("지각", "지각"),
        ("결석", "결석"),
        ("휴일", "휴일"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendances", verbose_name="사용자")
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="attendance", verbose_name="운영 기수"
    )
    workout_location = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, null=True, verbose_name="지점"
    )
    week = models.IntegerField(null=True, verbose_name="주차")
    request_time = models.DateTimeField(null=True, verbose_name="출석 요청 시간")
    request_processed_status = models.CharField(
        max_length=20, choices=REQUEST_STATUS_CHOICES, default="대기", null=True, verbose_name="처리 상태"
    )
    request_processed_time = models.DateTimeField(null=True, verbose_name="처리 시간")
    request_processed_user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, related_name="processed_requests", verbose_name="처리한 사용자"
    )
    attendance_status = models.CharField(
        max_length=20, choices=ATTENDANCE_STATUS_CHOICES, null=True, verbose_name="출석 상태"
    )
    is_alternate = models.BooleanField(default=False, verbose_name="대체 출석 여부")

    class Meta:
        db_table = "attendance"
        ordering = ["-request_time"]
        verbose_name = "출석"
        verbose_name_plural = "출석"


class AttendanceStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance_stats", verbose_name="사용자")
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="attendance_stats", verbose_name="운영 기수"
    )
    attendance = models.IntegerField(default=0, verbose_name="출석 횟수")
    late = models.IntegerField(default=0, verbose_name="지각 횟수")
    absence = models.IntegerField(default=0, verbose_name="결석 횟수")

    class Meta:
        db_table = "attendance_stats"
        verbose_name = "출석 통계"
        verbose_name_plural = "출석 통계"


class UnavailableDates(models.Model):
    date = models.DateField(verbose_name="휴일")

    class Meta:
        db_table = "unavailable_dates"
        verbose_name = "휴일"
        verbose_name_plural = "휴일"


class WeeklyStaffInfo(models.Model):
    DAY_OF_WEEK_CHOICES = (
        ("월요일", "월요일"),
        ("화요일", "화요일"),
        ("수요일", "수요일"),
        ("목요일", "목요일"),
        ("금요일", "금요일"),
    )

    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="weekly_staff_info", verbose_name="기수"
    )
    staff = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="운영진")
    day_of_week = models.CharField(max_length=10, choices=DAY_OF_WEEK_CHOICES, verbose_name="요일")
    workout_location = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, null=True, verbose_name="지점"
    )
    start_time = models.TimeField(verbose_name="운동 시작 시간")

    class Meta:
        db_table = "weekly_staff_info"
        verbose_name = "주간 운영진 정보"
        verbose_name_plural = "주간 운영진 정보"
