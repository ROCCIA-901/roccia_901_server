from django.db.models import Sum
from rest_framework import serializers

from account.models import User
from record.models import BoulderProblem
from record.serializers import WorkoutLevelChoiceField


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "generation",
            "role",
            "workout_location",
            "workout_level",
            "profile_number",
            "introduction",
        ]


class LevelCountSerializer(serializers.Serializer):
    workout_level = WorkoutLevelChoiceField(choices=User.WORKOUT_LEVELS)
    total_count = serializers.IntegerField()


class MypageSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source="*")
    records = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["profile", "records"]

    def get_records(self, obj):
        level_counts = (
            BoulderProblem.objects.filter(record__user=obj)
            .values("workout_level")
            .annotate(total_count=Sum("count"))
            .order_by("workout_level")
        )
        return LevelCountSerializer(level_counts, many=True).data
