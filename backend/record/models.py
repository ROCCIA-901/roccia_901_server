# mypy: ignore-errors

from django.db import models

from account.models import User
from attendance.models import Generation
from common.choices import WORKOUT_LEVELS, WORKOUT_LOCATION_CHOICES


class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="records", verbose_name="사용자")
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="record", verbose_name="운영 기수"
    )
    workout_location = models.CharField(max_length=100, choices=WORKOUT_LOCATION_CHOICES, verbose_name="지점")
    start_time = models.DateTimeField(verbose_name="운동 시작 시간")
    end_time = models.DateTimeField(verbose_name="운동 종료 시간")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")

    class Meta:
        db_table = "record"
        verbose_name = "기록"
        verbose_name_plural = "기록"


class BoulderProblem(models.Model):
    record = models.ForeignKey(Record, on_delete=models.CASCADE, related_name="boulder_problems", verbose_name="기록")
    workout_level = models.IntegerField(choices=WORKOUT_LEVELS, verbose_name="난이도")
    count = models.PositiveIntegerField(verbose_name="해결한 문제 개수")

    class Meta:
        db_table = "boulder_problem"
        verbose_name = "해결한 문제"
        verbose_name_plural = "해결한 문제"
