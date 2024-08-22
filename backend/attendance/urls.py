# mypy: ignore-errors

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import (
    AttendanceLocationAPIView,
    AttendanceRequestViewSet,
    AttendanceUserViewSet,
    AttendanceViewSet,
)

router = DefaultRouter()
router.register(r'users', AttendanceUserViewSet, basename='attendance-user')
router.register(r'requests', AttendanceRequestViewSet, basename='attendance-request')
router.register(r'', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path("location/", AttendanceLocationAPIView.as_view(), name="location"),

    path("", include((router.urls, "attendance"), namespace="attendance")),
]
