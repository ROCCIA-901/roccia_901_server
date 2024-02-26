from django.db import models


class Attendance(models.Model):
    WORKOUT_LOCATION_CHOICES: tuple[tuple[str, str], ...] = (
        ("더클라임 일산", "더클라임 일산"),
        ("더클라임 연남", "더클라임 연남"),
        ("더클라임 양재", "더클라임 양재"),
        ("더클라임 신림", "더클라임 신림"),
    )

    REQUEST_STATUS_CHOICES: tuple[tuple[str, str], ...] = (
        ("승인", "승인"),
        ("거절", "거절"),
    )

    ATTENDANCE_STATUS_CHOICES: tuple[tuple[str, str], ...] = (
        ("출석", "출석"),
        ("지각", "지각"),
        ("결석", "결석"),
        ("대체 출석", "대체 출석"),
    )

    user_id: models.IntegerField = models.IntegerField(help_text="사용자 ID")
    workout_location: models.CharField = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, null=True, help_text="운동 지점"
    )
    week: models.IntegerField = models.IntegerField(null=True, help_text="주차")
    request_time: models.DateTimeField = models.DateTimeField(help_text="출석 요청 시간")
    request_processed_status: models.CharField = models.CharField(
        max_length=20, choices=REQUEST_STATUS_CHOICES, null=True, help_text="요청 상태"
    )
    request_processed_time: models.DateTimeField = models.DateTimeField(null=True, help_text="요청 처리 시간")
    request_processed_user_id: models.IntegerField = models.IntegerField(null=True, help_text="요청을 처리한 사용자 ID")
    attendance_status: models.CharField = models.CharField(
        max_length=20, choices=ATTENDANCE_STATUS_CHOICES, null=True, help_text="출석 상태"
    )

    class Meta:
        db_table = "attendance"


class UnavailableDate(models.Model):
    WORKOUT_LOCATION_CHOICES: tuple[tuple[str, str], ...] = (
        ("더클라임 일산", "더클라임 일산"),
        ("더클라임 연남", "더클라임 연남"),
        ("더클라임 양재", "더클라임 양재"),
        ("더클라임 신림", "더클라임 신림"),
    )

    workout_location: models.CharField = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, help_text="운동 지점"
    )
    start_date: models.DateField = models.DateField()
    end_date: models.DateField = models.DateField()

    class Meta:
        db_table = "unavailable_date"
