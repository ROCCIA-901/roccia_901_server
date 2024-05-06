from django.db.models import DurationField, ExpressionWrapper, F, Sum
from rest_framework import serializers

from account.models import User
from config.exceptions import InvalidFieldException
from record.models import BoulderProblem, Record
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
    total_workout_time = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["profile", "total_workout_time", "records"]

    def get_records(self, obj):
        level_counts = (
            BoulderProblem.objects.filter(record__user=obj)
            .values("workout_level")
            .annotate(total_count=Sum("count"))
            .order_by("workout_level")
        )
        return LevelCountSerializer(level_counts, many=True).data

    def get_total_workout_time(self, obj):
        total_time_dict = (
            Record.objects.filter(user=obj)
            .annotate(workout_time=ExpressionWrapper(F("end_time") - F("start_time"), output_field=DurationField()))
            .aggregate(total=Sum("workout_time"))
        )
        dict_result = total_time_dict["total"]
        if dict_result is None:
            return 0

        total_seconds = dict_result.total_seconds()
        total_minutes = int(total_seconds // 60)
        return total_minutes


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
