from typing import Any

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from common.choices import ROLE_CHOICES, WORKOUT_LEVELS, WORKOUT_LOCATION_CHOICES
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


class Generation(models.Model):
    name = models.CharField(max_length=10, unique=True, primary_key=True, help_text="기수 이름")  # type: ignore
    start_date = models.DateField(null=True, help_text="기수 시작 날짜")  # type: ignore
    end_date = models.DateField(null=True, help_text="기수 종료 날짜")  # type: ignore

    class Meta:
        db_table = "generation"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=320, unique=True, null=False, blank=False, help_text="이메일")  # type: ignore
    username = models.CharField(max_length=20, help_text="사용자 이름")  # type: ignore
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, related_name="user", help_text="기수"
    )  # type: ignore
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="부원", help_text="역할")  # type: ignore
    workout_location = models.CharField(
        max_length=100, choices=WORKOUT_LOCATION_CHOICES, help_text="운동 지점"
    )  # type: ignore
    workout_level = models.IntegerField(choices=WORKOUT_LEVELS, help_text="운동 난이도")  # type: ignore
    profile_number = models.IntegerField(help_text="프로필 번호")  # type: ignore
    introduction = models.TextField(max_length=500, help_text="소개글")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, help_text="생성 일시")  # type: ignore
    updated_at = models.DateTimeField(auto_now=True, help_text="수정 일시")  # type: ignore

    is_active = models.BooleanField(default=False, help_text="활성 상태")  # type: ignore
    is_staff = models.BooleanField(default=False, help_text="스태프 상태")  # type: ignore

    objects = UserManager()

    USERNAME_FIELD: str = "email"

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        db_table = "user"
