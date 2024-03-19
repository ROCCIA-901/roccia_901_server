from django.db import models

from account.models import User


class WeeklyRanking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="weekly_ranking", help_text="사용자 ID"
    )  # type: ignore
    week = models.PositiveIntegerField()  # type: ignore
    rank = models.PositiveIntegerField()  # type: ignore
    score = models.FloatField(default=0.0)  # type: ignore

    class Meta:
        db_table = "weekly_ranking"
        ordering = ["week"]
