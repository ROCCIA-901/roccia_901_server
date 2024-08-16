from datetime import datetime

from rest_framework import serializers

from account.models import User
from account.serializers import UserRetrieveSerializer
from attendance.models import Attendance, AttendanceStats
from config.utils import WorkoutLevelChoiceField


class AttendanceSerializer(serializers.ModelSerializer):
    user = UserRetrieveSerializer(read_only=True)
    workout_level = WorkoutLevelChoiceField(choices=User.WORKOUT_LEVELS, source="user.workout_level")

    class Meta:
        model = Attendance
        fields = "__all__"
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context["request_type"] == "attendance_request_list":
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
                "workout_level": self.fields["workout_level"].to_representation(instance.user.workout_level),
            }

        return representation


class AttendanceDetailSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source="request_time", format="%Y년 %m월 %d일")
    time = serializers.DateTimeField(source="request_time", format="%-H시 %M분")

    class Meta:
        model = Attendance
        fields = ["week", "workout_location", "attendance_status", "date", "time"]


class AttendanceStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceStats
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    attendance_stats = AttendanceStatsSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "profile_number",
            "workout_location",
            "workout_level",
            "generation",
            "attendance_stats",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        data = {
            "user_id": representation["id"],
            "username": representation["username"],
            "profile_number": representation["profile_number"],
            "workout_location": representation["workout_location"],
            "workout_level": representation["workout_level"],
            "generation": representation["generation"],
        }

        if representation.get("attendance_stats"):
            data["attendance_rate"] = representation["attendance_stats"]["attendance_rate"]
        else:
            data["attendance_rate"] = None

        return data
