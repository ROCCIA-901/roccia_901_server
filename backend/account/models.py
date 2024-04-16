from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from config.exceptions import InvalidFieldException


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str, **extra_fields: Any) -> "User":
        if not email:
            raise InvalidFieldException("사용자는 이메일을 가지고 있어야 합니다.")
        email = self.normalize_email(email)
        user: User = self.model(email=email, **extra_fields)
        user.set_password(password)

        if extra_fields.get("role") == "운영진":
            user.is_staff = True

        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> "User":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise InvalidFieldException("슈퍼 유저의 is_staff 필드는 True여야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise InvalidFieldException("슈퍼 유저의 is_superuser 필드는 True여야 합니다.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES: tuple[tuple[str, str], ...] = (
        ("운영진", "운영진"),
        ("부원", "부원"),
        ("관리자", "관리자"),
    )

    WORKOUT_LOCATION_CHOICES: tuple[tuple[str, str], ...] = (
        ("더클라임 일산", "더클라임 일산"),
        ("더클라임 연남", "더클라임 연남"),
        ("더클라임 양재", "더클라임 양재"),
        ("더클라임 신림", "더클라임 신림"),
        ("더클라임 마곡", "더클라임 마곡"),
    )

    WORKOUT_LEVELS: tuple[tuple[int, str], ...] = (
        (1, "하얀색"),
        (2, "노란색"),
        (3, "주황색"),
        (4, "초록색"),
        (5, "파란색"),
        (6, "빨간색"),
        (7, "보라색"),
        (8, "회색"),
        (9, "갈색"),
        (10, "검정색"),
    )

    GENERATION_CHOICES: tuple[tuple[str, str], ...] = (
        ("1기", "1기"),
        ("2기", "2기"),
        ("3기", "3기"),
        ("4기", "4기"),
        ("5기", "5기"),
        ("6기", "6기"),
        ("7기", "7기"),
        ("8기", "8기"),
        ("9기", "9기"),
        ("10기", "10기"),
        ("11기", "11기"),
    )

    email = models.EmailField(max_length=320, unique=True, null=False, blank=False, help_text="이메일")  # type: ignore
    username = models.CharField(max_length=20, help_text="사용자 이름")  # type: ignore
    generation = models.CharField(max_length=10, choices=GENERATION_CHOICES, help_text="기수")  # type: ignore
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="부원", help_text="역할")  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, help_text="운동 지점"
    )  # type: ignore
    workout_level = models.IntegerField(choices=WORKOUT_LEVELS, help_text="운동 난이도")  # type: ignore
    profile_number = models.IntegerField(help_text="프로필 번호")  # type: ignore
    introduction = models.TextField(max_length=500, help_text="소개글")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 일시")  # type: ignore
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 일시")  # type: ignore

    is_active = models.BooleanField(default=True, help_text="활성 상태")  # type: ignore
    is_staff = models.BooleanField(default=False, help_text="스태프 상태")  # type: ignore

    objects = UserManager()

    USERNAME_FIELD: str = "email"

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        db_table = "user"


class UserRegistrationEmailAuthStatus(models.Model):
    email = models.EmailField(unique=True, help_text="이메일")  # type: ignore
    code = models.IntegerField(help_text="인증 번호")  # type: ignore
    created_at = models.DateTimeField(auto_now=True, help_text="생성 시간")  # type: ignore
    status = models.BooleanField(default=False, help_text="인증 상태")  # type: ignore

    class Meta:
        db_table = "user_register_auth_status"


class PasswordUpdateEmailAuthStatus(models.Model):
    email = models.EmailField(unique=True, help_text="이메일")  # type: ignore
    code = models.IntegerField(help_text="인증 번호")  # type: ignore
    created_at = models.DateTimeField(auto_now=True, help_text="생성 시간")  # type: ignore

    class Meta:
        db_table = "password_update_email_auth_status"
