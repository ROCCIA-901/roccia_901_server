from django.db.models import DurationField, ExpressionWrapper, F, Sum
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from account.models import User
from attendance.models import AttendanceStats
from attendance.services import get_current_generation
from common.choices import WORKOUT_LEVELS, WORKOUT_LOCATION_CHOICES
from config.exceptions import InvalidFieldException, NotExistException
from mypage.schemas import USER_UPDATE_REQUEST_EXAMPLE
from record.models import BoulderProblem, Record
from record.serializers import WorkoutLevelChoiceField


class UserProfileSerializer(serializers.ModelSerializer):
    """
    다른 유저 프로필 조회를 위한 시리얼라이저입니다.
    """

    workout_level = WorkoutLevelChoiceField(choices=WORKOUT_LEVELS)

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
    """
    해결한 난이도의 각 개수를 조회를 위한 시리얼라이저입니다.
    """

    workout_level = WorkoutLevelChoiceField(choices=WORKOUT_LEVELS)
    total_count = serializers.IntegerField()


class AttendanceStatsSerializer(serializers.ModelSerializer):
    """
    출석 통계 조회를 위한 시리얼라이저입니다.
    """

    class Meta:
        model = AttendanceStats
        fields = ["attendance", "late", "absence"]


class MypageSerializer(serializers.ModelSerializer):
    """
    내 프로필 조회를 위한 시리얼라이저입니다.
    """

    profile = UserProfileSerializer(source="*")
    total_workout_time = serializers.SerializerMethodField()
    records = serializers.SerializerMethodField()
    attendance_stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["profile", "total_workout_time", "records", "attendance_stats"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.current_generation = get_current_generation()
        except NotExistException:
            self.current_generation = None

    def get_records(self, obj):
        if not self.current_generation:
            return []

        level_counts = (
            BoulderProblem.objects.filter(record__user=obj, record__generation=self.current_generation)
            .values("workout_level")
            .annotate(total_count=Sum("count"))
            .order_by("workout_level")
        )
        return LevelCountSerializer(level_counts, many=True).data

    def get_total_workout_time(self, obj):
        if not self.current_generation:
            return 0

        total_time_dict = (
            Record.objects.filter(user=obj, generation=self.current_generation)
            .annotate(workout_time=ExpressionWrapper(F("end_time") - F("start_time"), output_field=DurationField()))
            .aggregate(total=Sum("workout_time"))
        )
        dict_result = total_time_dict["total"]
        if dict_result is None:
            return 0

        total_seconds = dict_result.total_seconds()
        total_minutes = int(total_seconds // 60)
        return total_minutes

    def get_attendance_stats(self, obj):
        if not self.current_generation:
            return {}

        attendance_stats = AttendanceStats.objects.filter(user=obj, generation=self.current_generation).first()
        return AttendanceStatsSerializer(attendance_stats).data if attendance_stats else {}


@extend_schema_serializer(examples=USER_UPDATE_REQUEST_EXAMPLE)
class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["workout_location", "workout_level", "profile_number", "introduction"]

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in WORKOUT_LOCATION_CHOICES]
        if value not in workout_location:
            raise InvalidFieldException("지점이 정확하지 않습니다.")
        return value

    def validate_workout_level(self, value: int) -> int:
        workout_level = [choice[0] for choice in WORKOUT_LEVELS]
        if value not in workout_level:
            raise InvalidFieldException("난이도가 정확하지 않습니다.")
        return value

    def validate_profile_number(self, value: str) -> str:
        if value not in range(1, 9):
            raise InvalidFieldException("프로필 번호가 정확하지 않습니다.")
        return value
