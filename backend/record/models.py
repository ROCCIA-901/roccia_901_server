from django.db import models

from account.models import User


class Record(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="records", help_text="사용자 ID"
    )  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=User.WORKOUT_LOCATION_CHOICES, help_text="운동 지점"
    )  # type: ignore
    start_time = models.DateTimeField(help_text="운동 시작 시간")  # type: ignore
    end_time = models.DateTimeField(help_text="운동 종료 시간")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 일시")  # type: ignore
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 일시")  # type: ignore

    class Meta:
        db_table = "record"


class BoulderProblem(models.Model):
    record = models.ForeignKey(
        Record, on_delete=models.CASCADE, related_name="boulder_problems", help_text="운동 기록 ID"
    )  # type: ignore
    workout_level = models.CharField(max_length=100, choices=User.WORKOUT_LEVELS, help_text="운동 난이도")  # type: ignore
    count = models.PositiveIntegerField(help_text="푼 문제 개수")  # type: ignore

    class Meta:
        db_table = "boulder_problem"
