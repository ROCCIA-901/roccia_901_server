import re
from datetime import timedelta
from typing import Any

from django.contrib.auth import authenticate
from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from account.models import PasswordUpdateEmailAuthStatus, User
from config.exceptions import (
    EmptyFieldException,
    InvalidAccountException,
    InvalidFieldException,
    InvalidFieldStateException,
)


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
    workout_level = WorkoutLevelChoiceField(
        User.WORKOUT_LEVELS,
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

        if cache.get(f"{value}:register:status") is None or cache.get(f"{value}:register:status") == "uncertified":
            raise InvalidFieldStateException("인증이 안 된 이메일입니다.")

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

    def validate_workout_level(self, value: int) -> int:
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


class UserRegisterEmailVerificationSerializer(serializers.Serializer):
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


class UserRegisterAuthCodeVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )
    code = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "인증번호는 필수 입력 항목입니다.",
            "blank": "인증번호는 비워 둘 수 없습니다.",
        },
    )

    def validate_email(self, value: str) -> str:
        if not cache.get(f"{value}:register:code"):
            raise InvalidFieldException("해당 이메일의 인증번호 요청 내역이 존재하지 않습니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        receiver = data["email"]
        entered_code = data["code"]

        if cache.get(f"{receiver}:register:status") == "certified":
            raise InvalidFieldStateException("이미 인증 완료된 사용자입니다.")

        if cache.get(f"{receiver}:register:code") != entered_code:
            raise InvalidFieldException("인증번호가 일치하지 않습니다.")

        return data


class PasswordUpdateEmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )

    def validate_email(self, value: str) -> str:
        if not User.objects.filter(email=value).exists():
            raise InvalidFieldException("존재하지 않는 이메일입니다.")
        return value


class PasswordUpdateAuthCodeVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )
    code = serializers.IntegerField(
        required=True,
        error_messages={
            "required": "인증번호는 필수 입력 항목입니다.",
            "blank": "인증번호는 비워 둘 수 없습니다.",
        },
    )

    def validate_email(self, value: str) -> str:
        if not PasswordUpdateEmailAuthStatus.objects.filter(email=value).exists():
            raise InvalidFieldException(
                "해당 이메일의 인증번호 요청 내역이 존재하지 않습니다. 인증번호 요청을 진행해주세요."
            )
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        email = data["email"]
        code = data["code"]

        auth_status = PasswordUpdateEmailAuthStatus.objects.get(email=email)

        if auth_status.code != code:
            raise InvalidFieldException("인증번호가 일치하지 않습니다.")

        if timezone.now() - auth_status.created_at > timedelta(minutes=10):
            raise InvalidFieldException("인증번호의 유효시간이 지났습니다.")

        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(
        required=True,
        error_messages={
            "required": "refresh 필드는 필수 항목입니다.",
            "blank": "refresh 필드는 비워 둘 수 없습니다.",
        },
    )

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except TokenError as e:
            raise serializers.ValidationError("토큰이 유효하지 않습니다.")

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        required=True,
        error_messages={
            "required": "refresh 필드는 필수 항목입니다.",
            "blank": "refresh 필드는 비워 둘 수 없습니다.",
        },
    )


class PasswordUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "이메일은 필수 입력 항목입니다.",
            "blank": "이메일은 비워 둘 수 없습니다.",
        },
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "required": "비밀번호는 필수 입력 항목입니다.",
            "blank": "비밀번호는 비워 둘 수 없습니다.",
        },
    )
    new_password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            "required": "비밀번호 확인은 필수 입력 항목입니다.",
            "blank": "비밀번호 확인은 비워 둘 수 없습니다.",
        },
    )

    def validate_email(self, value: str) -> str:
        if not User.objects.filter(email=value).exists():
            raise InvalidFieldException("존재하지 않는 이메일입니다.")
        return value

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        new_password = data.get("new_password")
        new_password_confirmation = data.get("new_password_confirmation")

        if new_password is None:
            raise EmptyFieldException("비밀번호는 필수 입력 항목입니다.")

        if new_password != new_password_confirmation:
            raise InvalidFieldException("비밀번호가 일치하지 않습니다.")

        if len(new_password) < 7:
            raise InvalidFieldException("비밀번호는 최소 7자 이상이어야 합니다.")

        if not any(char.isupper() for char in new_password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 대문자가 포함되어야 합니다.")

        if not any(char.islower() for char in new_password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 소문자가 포함되어야 합니다.")

        if not any(char.isdigit() for char in new_password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 숫자가 포함되어야 합니다.")

        special_characters = r"[~!@#$%^&*()_+{}\":;'<>?,./]"
        if not any(char in special_characters for char in new_password):
            raise InvalidFieldException("비밀번호에는 최소 1개 이상의 특수 문자가 포함되어야 합니다.")

        pattern = re.compile(r"[가-힣ㄱ-ㅎㅏ-ㅣ]")
        if pattern.search(new_password):
            raise InvalidFieldException("비밀번호에는 한글이 포함될 수 없습니다.")

        return data

    def save(self):
        email = self.validated_data["email"]
        new_password = self.validated_data["new_password"]

        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()
        return user
