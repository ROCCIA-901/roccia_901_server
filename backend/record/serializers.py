from typing import Any

from rest_framework import serializers

from account.models import User
from config.exceptions import InvalidFieldException
from record.models import BoulderProblem, Record


class BoulderProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoulderProblem
        fields: tuple = (
            "id",
            "workout_level",
            "count",
        )


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
            "user",
            "workout_location",
            "start_time",
            "end_time",
            "created_at",
            "updated_at",
            "boulder_problems",
        )

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in User.WORKOUT_LOCATION_CHOICES]
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

        instance.user = validated_data.get("user", instance.user)
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
            "created_at",
            "updated_at",
            "boulder_problems",
        )

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in User.WORKOUT_LOCATION_CHOICES]
        if value not in workout_location:
            raise InvalidFieldException("지점이 정확하지 않습니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if data.get("start_time") >= data.get("end_time"):  # type: ignore
            raise InvalidFieldException("시작 시간이 종료 시간보다 같거나 늦을 수 없습니다.")
        return data

    def create(self, validated_data: dict[str, Any]):
        probs = validated_data.pop("boulder_problems")
        record = Record.objects.create(**validated_data)
        for prob in probs:
            BoulderProblem.objects.create(record=record, **prob)
        return record
