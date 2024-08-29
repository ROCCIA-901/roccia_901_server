# mypy: ignore-errors

from django.db import models

from account.models import User
from attendance.models import Generation


class Ranking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ranking", verbose_name="사용자")
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="ranking", verbose_name="운영 기수"
    )
    week = models.PositiveIntegerField(verbose_name="주차")
    score = models.FloatField(default=0.0, verbose_name="점수 합산")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 시각")

    class Meta:
        db_table = "ranking"
        ordering = ["week"]
        verbose_name = "랭킹"
        verbose_name_plural = "랭킹"
