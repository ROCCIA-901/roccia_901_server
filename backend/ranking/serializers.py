from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from account.models import User
from config.exceptions import InvalidFieldException
from ranking.models import Ranking


class WorkoutLevelChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        for key, val in self._choices.items():
            if key == int(obj):
                return val

    def to_internal_value(self, data):
        # To support inserts with the value
        for key, val in self._choices.items():
            if val == data:
                return key
        raise InvalidFieldException("난이도가 정확하지 않습니다.")


class RankingSerializer(serializers.ModelSerializer):
    user_id = ReadOnlyField(source="user__id")
    username = ReadOnlyField(source="user__username")
    user_generation = ReadOnlyField(source="user__generation")
    user_workout_location = ReadOnlyField(source="user__workout_location")
    user_profile_number = ReadOnlyField(source="user__profile_number")
    user_workout_level = serializers.SerializerMethodField()

    def get_user_workout_level(self, obj) -> str:  # type: ignore
        for key, val in User.WORKOUT_LEVELS:
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
