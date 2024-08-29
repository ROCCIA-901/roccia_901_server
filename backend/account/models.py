# mypy: ignore-errors

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
    name = models.CharField(max_length=10, unique=True, primary_key=True, verbose_name="기수")
    start_date = models.DateField(null=True, blank=True, verbose_name="시작 날짜")
    end_date = models.DateField(null=True, blank=True, verbose_name="종료 날짜")

    class Meta:
        db_table = "generation"
        verbose_name = "기수"
        verbose_name_plural = "기수"


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=320, unique=True, null=False, blank=False, verbose_name="이메일")
    username = models.CharField(max_length=20, verbose_name="사용자 이름")
    generation = models.ForeignKey(
        Generation, on_delete=models.SET_NULL, null=True, blank=True, related_name="user", verbose_name="가입 기수"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="부원", verbose_name="역할")
    workout_location = models.CharField(max_length=100, choices=WORKOUT_LOCATION_CHOICES, verbose_name="지점")
    workout_level = models.IntegerField(choices=WORKOUT_LEVELS, verbose_name="난이도")
    profile_number = models.IntegerField(verbose_name="프로필 번호")
    introduction = models.TextField(max_length=500, verbose_name="소개글")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성 일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정 일시")

    is_active = models.BooleanField(default=False, verbose_name="활성 여부")
    is_staff = models.BooleanField(default=False, verbose_name="스태프 여부")

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self) -> str:
        return str(self.email)

    class Meta:
        db_table = "user"
        verbose_name = "부원"
        verbose_name_plural = "부원"
