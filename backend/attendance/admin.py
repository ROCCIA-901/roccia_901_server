# mypy: ignore-errors

from django.contrib import admin

from .models import Attendance, AttendanceStats, UnavailableDates, WeeklyStaffInfo


@admin.register(WeeklyStaffInfo)
class WeeklyStaffInfoAdmin(admin.ModelAdmin):
    list_display = ("get_generation_name", "get_staff_name", "day_of_week", "workout_location", "start_time")
    search_fields = ("staff__username", "generation__name")
    ordering = ("-generation", "day_of_week")

    def get_generation_name(self, obj):
        return obj.generation.name

    def get_staff_name(self, obj):
        return obj.staff.username

    get_generation_name.short_description = "운영 기수"

    get_staff_name.short_description = "운영진"


@admin.register(UnavailableDates)
class UnavailableDatesAdmin(admin.ModelAdmin):
    list_display = ("date",)
    ordering = ("-date",)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_name",
        "generation",
        "week",
        "attendance_status",
        "workout_location",
        "request_time",
        "request_processed_status",
        "request_processed_time",
        "get_request_processed_user_name",
        "is_alternate",
    )
    list_filter = ("generation", "request_processed_status", "attendance_status", "workout_location", "week")
    search_fields = ("user__username", "user__email", "generation__name")
    ordering = ("-request_time",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "generation")

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = "부원"

    def get_request_processed_user_name(self, obj):
        if obj.request_processed_user:
            return obj.request_processed_user.username
        return "-"

    get_request_processed_user_name.short_description = "처리한 운영진"


@admin.register(AttendanceStats)
class AttendanceStatsAdmin(admin.ModelAdmin):
    list_display = ("get_user_name", "generation", "attendance", "late", "absence")
    list_filter = ("generation",)
    search_fields = ("user__username", "user__email")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("user", "generation")

    def get_user_name(self, obj):
        return obj.user.username

    get_user_name.short_description = "부원"
