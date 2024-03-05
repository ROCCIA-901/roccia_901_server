import re
from typing import Any

from django.contrib.auth import authenticate
from rest_framework import serializers

from account.models import User
from config.exceptions import (
    EmptyFieldException,
    InvalidAccountException,
    InvalidFieldException,
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )
    username = serializers.CharField(
        required=True,
        error_messages={
            "required": "이름은 필수 입력 항목입니다.",
            "blank": "이름은 비워 둘 수 없습니다.",
        },
    )
    generation = serializers.CharField(
        required=True,
        error_messages={
            "required": "기수는 필수 입력 항목입니다.",
            "blank": "기수는 비워 둘 수 없습니다.",
        },
    )
    role = serializers.CharField(
        required=True,
        error_messages={
            "required": "역할은 필수 입력 항목입니다.",
            "blank": "역할은 비워 둘 수 없습니다.",
        },
    )
    workout_location = serializers.CharField(
        required=True,
        error_messages={
            "required": "운동 지점은 필수 입력 항목입니다.",
            "blank": "운동 지점은 비워 둘 수 없습니다.",
        },
    )
    workout_level = serializers.CharField(
        required=True,
        error_messages={
            "required": "운동 난이도는 필수 입력 항목입니다.",
            "blank": "운동 난이도는 비워 둘 수 없습니다.",
        },
    )
    profile_number = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "프로필 번호는 필수 입력 항목입니다.",
            "blank": "프로필 번호는 비워 둘 수 없습니다.",
        },
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "required": "비밀번호는 필수 입력 항목입니다.",
            "blank": "비밀번호는 비워 둘 수 없습니다.",
        },
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "required": "비밀번호 확인은 필수 입력 항목입니다.",
            "blank": "비밀번호 확인은 비워 둘 수 없습니다.",
        },
    )

    username_pattern = re.compile(r"^[가-힣]{2,4}$")

    class Meta:
        model: type[User] = User
        fields: tuple[str, ...] = (
            "email",
            "password",
            "password_confirmation",
            "username",
            "generation",
            "role",
            "workout_location",
            "workout_level",
            "profile_number",
            "introduction",
        )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise InvalidFieldException("이미 존재하는 이메일입니다.")
        return value

    def validate_username(self, value: str) -> str:
        if not self.username_pattern.match(value):
            raise InvalidFieldException("이름이 정확하지 않습니다.")
        return value

    def validate_generation(self, value: str) -> str:
        generation = [choice[0] for choice in User.GENERATION_CHOICES]
        if value not in generation:
            raise InvalidFieldException("기수가 정확하지 않습니다.")
        return value

    def validate_role(self, value: str) -> str:
        role = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in role:
            raise InvalidFieldException("역할이 정확하지 않습니다.")
        return value

    def validate_workout_location(self, value: str) -> str:
        workout_location = [choice[0] for choice in User.WORKOUT_LOCATION_CHOICES]
        if value not in workout_location:
            raise InvalidFieldException("지점이 정확하지 않습니다.")
        return value

    def validate_workout_level(self, value: str) -> str:
        workout_level = [choice[0] for choice in User.WORKOUT_LEVELS]
        if value not in workout_level:
            raise InvalidFieldException("난이도가 정확하지 않습니다.")
        return value

    def validate_profile_number(self, value: str) -> str:
        if value not in range(1, 9):
            raise InvalidFieldException("프로필 번호가 정확하지 않습니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        password = data.get("password")
        password_confirmation = data.get("password_confirmation")

        if password is None:
            raise EmptyFieldException("비밀번호는 필수 입력 항목입니다.")

        if password != password_confirmation:
            raise InvalidFieldException("비밀번호가 일치하지 않습니다.")

        if len(password) < 7:
            raise InvalidFieldException("비밀번호는 최소 7자 이상이어야 합니다.")

        if not any(char.isupper() for char in password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 대문자가 포함되어야 합니다.")

        if not any(char.islower() for char in password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 소문자가 포함되어야 합니다.")

        if not any(char.isdigit() for char in password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 숫자가 포함되어야 합니다.")

        special_characters = r"[~!@#$%^&*()_+{}\":;'<>?,./]"
        if not any(char in special_characters for char in password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 특수 문자가 포함되어야 합니다.")

        pattern = re.compile(r"[가-힣ㄱ-ㅎㅏ-ㅣ]")
        if pattern.search(password):
            raise InvalidFieldException("비밀번호에는 한글이 포함될 수 없습니다.")

        return data

    def create(self, validated_data: dict[str, Any]) -> User:
        validated_data.pop("password_confirmation", None)
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            "required": "비밀번호는 필수 입력 항목입니다.",
            "blank": "비밀번호는 비워 둘 수 없습니다.",
        },
    )

    def validate_email(self, value: str) -> str:
        if not User.objects.filter(email=value).exists():
            raise InvalidAccountException("등록되지 않은 이메일입니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        user = authenticate(email=data["email"], password=data["password"])
        if user is None:
            raise InvalidFieldException("이메일 또는 비밀번호가 유효하지 않습니다.")

        data["user"] = user
        return data


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "generation",
            "role",
            "workout_location",
            "workout_level",
            "profile_number",
            "introduction",
        ]


class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise InvalidFieldException("이미 존재하는 이메일입니다.")
        return value
