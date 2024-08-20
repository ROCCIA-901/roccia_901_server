from django.db import models

from account.models import User
from attendance.models import Generation


class Ranking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="ranking", help_text="사용자 ID"
    )  # type: ignore
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="ranking", help_text="기수"
    )  # type: ignore
    week = models.PositiveIntegerField(help_text="운동 주차")  # type: ignore
    score = models.FloatField(default=0.0, help_text="운동 점수")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 시각")  # type: ignore

    class Meta:
        db_table = "ranking"
        ordering = ["week"]
