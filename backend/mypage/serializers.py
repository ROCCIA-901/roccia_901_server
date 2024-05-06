from django.db.models import Sum
from rest_framework import serializers

from account.models import User
from config.exceptions import InvalidFieldException
from record.models import BoulderProblem
from record.serializers import WorkoutLevelChoiceField


class UserProfileSerializer(serializers.ModelSerializer):
    workout_level = WorkoutLevelChoiceField(choices=User.WORKOUT_LEVELS)

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


class UserUpdateSerializer(serializers.ModelSerializer):
    workout_location = serializers.CharField(
        error_messages={
            "blank": "운동 지점은 비워 둘 수 없습니다.",
        },
    )
    workout_level = WorkoutLevelChoiceField(
        User.WORKOUT_LEVELS,
        error_messages={
            "blank": "운동 난이도는 비워 둘 수 없습니다.",
        },
    )
    profile_number = serializers.IntegerField(
        error_messages={
            "blank": "프로필 번호는 비워 둘 수 없습니다.",
        },
    )

    class Meta:
        model = User
        fields = ["workout_location", "workout_level", "profile_number", "introduction"]
        extra_kwargs = {"introduction": {"required": False}}

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in User.WORKOUT_LOCATION_CHOICES]
        if value not in workout_location:
            raise InvalidFieldException("지점이 정확하지 않습니다.")
        return value

    def validate_profile_number(self, value: str) -> str:
        if value not in range(1, 9):
            raise InvalidFieldException("프로필 번호가 정확하지 않습니다.")
        return value
