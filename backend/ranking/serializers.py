from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from ranking.models import Ranking


class RankingSerializer(serializers.ModelSerializer):
    username = ReadOnlyField(source="user.username")
    user_generation = ReadOnlyField(source="user.generation")
    user_workout_location = ReadOnlyField(source="user.workout_location")
    user_workout_level = ReadOnlyField(source="user.workout_level")
    user_profile_number = ReadOnlyField(source="user.profile_number")

    class Meta:
        model: type[Ranking] = Ranking
        fields: tuple = (
            "score",
            "username",
            "user_generation",
            "user_workout_location",
            "user_workout_level",
            "user_profile_number",
        )
