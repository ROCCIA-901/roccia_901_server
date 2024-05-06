from datetime import datetime
from typing import Any

import pytz
from django.db.models.functions.datetime import TruncDate
from rest_framework import serializers

from account.models import User
from config.exceptions import InvalidFieldException
from record.models import BoulderProblem, Record


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


class BoulderProblemSerializer(serializers.ModelSerializer):
    workout_level = WorkoutLevelChoiceField(choices=User.WORKOUT_LEVELS)

    class Meta:
        model = BoulderProblem
        fields: tuple = (
            "workout_level",
            "count",
        )

    def validate_workout_level(self, value: int) -> int:
        workout_level = [choice[0] for choice in User.WORKOUT_LEVELS]
        if value not in workout_level:
            raise InvalidFieldException("난이도가 정확하지 않습니다.")
        return value


class RecordSerializer(serializers.ModelSerializer):
    workout_location = serializers.CharField(
        required=True,
        error_messages={
            "required": "운동지점은 필수 입력 항목입니다.",
            "blank": "운동지점은 비워 둘 수 없습니다.",
        },
    )
    start_time = serializers.DateTimeField(
        required=True,
        error_messages={
            "required": "운동 시작 시간은 필수 입력 항목입니다.",
            "blank": "운동 시작 시간은 비워 둘 수 없습니다.",
        },
    )
    end_time = serializers.DateTimeField(
        required=True,
        error_messages={
            "required": "운동 종료 시간은 필수 입력 항목입니다.",
            "blank": "운동 종료 시간은 비워 둘 수 없습니다.",
        },
    )
    boulder_problems = BoulderProblemSerializer(many=True)

    class Meta:
        model: type[Record] = Record
        fields: tuple[str, ...] = (
            "id",
            "workout_location",
            "start_time",
            "end_time",
            "boulder_problems",
        )

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in Record.WORKOUT_LOCATION_CHOICES]
        if value not in workout_location:
            raise InvalidFieldException("지점이 정확하지 않습니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("start_time") >= data.get("end_time"):  # type: ignore
            raise InvalidFieldException("시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.")
        if data.get("start_time").date() != data.get("end_time").date():  # type: ignore
            raise InvalidFieldException("시작 날짜와 종료 날짜는 같아야 합니다.")
        return data

    def create(self, validated_data: dict[str, Any]):
        probs = validated_data.pop("boulder_problems")
        record = Record.objects.create(**validated_data)
        for prob in probs:
            BoulderProblem.objects.create(record=record, **prob)
        return record

    def update(self, instance, validated_data: dict[str, Any]) -> dict[str, Any]:
        probs_data = validated_data.pop("boulder_problems")

        instance.workout_location = validated_data.get("workout_location", instance.workout_location)
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.save()

        BoulderProblem.objects.filter(record=instance.id).delete()
        for prob_data in probs_data:
            BoulderProblem.objects.create(record=instance, **prob_data)

        return instance


class BoulderProblemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoulderProblem
        fields: tuple = (
            "workout_level",
            "count",
        )


class RecordCreateSerializer(serializers.ModelSerializer):
    boulder_problems = BoulderProblemSerializer(many=True)

    class Meta:
        model: type[Record] = Record
        fields: tuple[str, ...] = (
            "user",
            "workout_location",
            "start_time",
            "end_time",
            "boulder_problems",
        )

    def validate_end_time(self, value: datetime) -> datetime:
        korea_tz = pytz.timezone("Asia/Seoul")
        current_time = datetime.now(korea_tz)
        if current_time < value:
            raise InvalidFieldException("운동 종료 후 기록할 수 있습니다.")
        return value

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in Record.WORKOUT_LOCATION_CHOICES]
        if value not in workout_location:
            raise InvalidFieldException("지점이 정확하지 않습니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        current_date = datetime.today().date()
        if (
            Record.objects.filter(user=data.get("user"))
            .annotate(date=TruncDate("end_time"))
            .filter(date=current_date)
            .exists()
        ):
            raise InvalidFieldException("해당일에 이미 기록이 존재합니다.")

        if data.get("start_time") >= data.get("end_time"):  # type: ignore
            raise InvalidFieldException("시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.")
        return data

    def create(self, validated_data: dict[str, Any]):
        probs = validated_data.pop("boulder_problems")
        record = Record.objects.create(**validated_data)
        for prob in probs:
            BoulderProblem.objects.create(record=record, **prob)
        return record
