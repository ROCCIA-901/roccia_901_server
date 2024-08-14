from django.db import models

from account.models import User


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
        ("대체 출석", "대체 출석"),
        ("휴일", "휴일"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="attendance")  # type: ignore
    generation = models.CharField(choices=User.GENERATION_CHOICES, help_text="기수")  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=User.WORKOUT_LOCATION_CHOICES, null=True, help_text="운동 지점"
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

    class Meta:
        db_table = "attendance"
        ordering = ["-request_time"]


class AttendanceStats(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attendance_stats")  # type: ignore
    generation = models.CharField(choices=User.GENERATION_CHOICES, help_text="기수")  # type: ignore
    attendance = models.IntegerField(default=0, help_text="출석 횟수")  # type: ignore
    late = models.IntegerField(default=0, help_text="지각 횟수")  # type: ignore
    absence = models.IntegerField(default=0, help_text="결석 횟수")  # type: ignore
    substitute = models.IntegerField(default=0, help_text="대체 출석 횟수")  # type: ignore
    attendance_rate = models.FloatField(help_text="출석률")  # type: ignore

    class Meta:
        db_table = "attendance_stats"


class ActivityDates(models.Model):
    generation = models.CharField(max_length=10, choices=User.GENERATION_CHOICES, help_text="기수")  # type: ignore
    start_date = models.DateField(help_text="기수 시작 날짜")  # type: ignore
    end_date = models.DateField(help_text="기수 종료 날짜")  # type: ignore

    class Meta:
        db_table = "activity_dates"


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

    generation = models.CharField(choices=User.GENERATION_CHOICES, help_text="기수")  # type: ignore
    staff = models.ForeignKey(User, on_delete=models.CASCADE, help_text="운영진")  # type: ignore
    day_of_week = models.CharField(choices=DAY_OF_WEEK_CHOICES, help_text="요일")  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=User.WORKOUT_LOCATION_CHOICES, null=True, help_text="운동 지점"
    )  # type: ignore
    start_time = models.TimeField(help_text="운동 시작 시간")  # type: ignore

    class Meta:
        db_table = "weekly_staff_info"
