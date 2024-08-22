from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from common.choices import WORKOUT_LEVELS
from ranking.models import Ranking


class RankingSerializer(serializers.ModelSerializer):
    user_id = ReadOnlyField(source="user__id")
    username = ReadOnlyField(source="user__username")
    user_generation = ReadOnlyField(source="user__generation")
    user_workout_location = ReadOnlyField(source="user__workout_location")
    user_profile_number = ReadOnlyField(source="user__profile_number")
    user_workout_level = serializers.SerializerMethodField()

    def get_user_workout_level(self, obj) -> str:  # type: ignore
        for key, val in WORKOUT_LEVELS:
            if key == obj["user__workout_level"]:
                return val
        return ""

    class Meta:
        model: type[Ranking] = Ranking
        fields: tuple = (
            "score",
            "user_id",
            "username",
            "user_generation",
            "user_workout_location",
            "user_workout_level",
            "user_profile_number",
        )
