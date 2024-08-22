from datetime import datetime

from rest_framework import serializers

from account.models import Generation, User
from account.serializers import UserRetrieveSerializer
from attendance.models import Attendance, AttendanceStats
from attendance.services import calculate_attendance_rate, get_current_generation
from common.choices import WORKOUT_LEVELS
from config.utils import WorkoutLevelChoiceField


class AttendanceRequestSerializer(serializers.ModelSerializer):
    """
    출석 요청을 처리하기 위한 시리얼라이저입니다.
    """

    class Meta:
        model = Attendance
        fields = "__all__"


class AttendanceRequestListSerializer(serializers.ModelSerializer):
    """
    출석 요청 목록을 반환하기 위한 시리얼라이저입니다.
    """

    user = UserRetrieveSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        date_str = representation["request_time"]
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
        representation["request_time"] = date_obj.strftime("%-m월 %d일 %H:%M")

        return {
            "id": representation["id"],
            "request_time": representation["request_time"],
            "user_id": representation["user"]["id"],
            "username": representation["user"]["username"],
            "generation": representation["user"]["generation"],
            "profile_number": representation["user"]["profile_number"],
            "workout_location": representation["user"]["workout_location"],
        }


class AttendanceDetailSerializer(serializers.ModelSerializer):
    """
    출석 내역 조회 위한 시리얼라이저입니다.
    """

    request_date = serializers.DateTimeField(source="request_time", format="%Y년 %m월 %d일")
    request_time = serializers.DateTimeField(format="%-H시 %M분")

    class Meta:
        model = Attendance
        fields = ["week", "workout_location", "attendance_status", "request_date", "request_time"]


class UserListSerializer(serializers.ModelSerializer):
    """
    부원 목록 조회를 위한 시리얼라이저입니다.
    """

    workout_level = WorkoutLevelChoiceField(choices=WORKOUT_LEVELS)
    attendance_rate = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_number",
            "workout_location",
            "workout_level",
            "generation",
            "attendance_rate",
        ]

    def get_attendance_rate(self, instance):
        current_generation: Generation = get_current_generation()
        current_gen_number: int = int(current_generation.name[:-1])
        user_gen_number: int = int(instance.generation.name[:-1])
        attendance_stats: AttendanceStats = AttendanceStats.objects.filter(
            user=instance, generation=current_generation
        ).first()

        if not attendance_stats:
            return 0

        return calculate_attendance_rate(attendance_stats, current_gen_number, user_gen_number)

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        return {
            "user_id": representation["id"],
            "username": representation["username"],
            "profile_number": representation["profile_number"],
            "workout_location": representation["workout_location"],
            "workout_level": self.fields["workout_level"].to_representation(instance.workout_level),
            "generation": representation["generation"],
            "attendance_rate": self.get_attendance_rate(instance),
        }
