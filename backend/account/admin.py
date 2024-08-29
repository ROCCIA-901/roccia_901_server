# mypy: ignore-errors

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .models import Generation, User

admin.site.unregister(Group)
admin.site.unregister(DjangoJob)
admin.site.unregister(DjangoJobExecution)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 사용자 목록에 표시할 필드
    list_display = ("email", "username", "role", "workout_location", "workout_level", "is_active", "is_staff")

    # `is_active` 필드를 직접 변경할 수 있도록 추가
    list_editable = ("is_active",)

    # 사용자가 검색할 수 있는 필드
    search_fields = ("email", "username")

    # 필터링 옵션
    list_filter = ("role", "workout_location", "workout_level", "is_active", "is_staff")

    # 사용자 편집 페이지에 표시할 필드 구성
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("username", "introduction", "profile_number")}),
        (
            _("Roles and permissions"),
            {
                "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        (
            _("Details"),
            {
                "fields": ("role", "generation", "workout_location", "workout_level"),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "created_at", "updated_at")}),
    )

    # 사용자 생성 및 수정 페이지에 입력할 때 필드에 대한 도움말 제공
    readonly_fields = ("created_at", "updated_at")

    ordering = ("email",)


@admin.register(Generation)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")
    search_fields = ("name",)
    ordering = ("-start_date",)
