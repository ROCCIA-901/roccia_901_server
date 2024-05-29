# mypy: ignore-errors

# from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import (
    AttendanceRequestViewSet,
    AttendanceUserViewSet,
    AttendanceViewSet,
)

router = DefaultRouter()
router.register(r'users', AttendanceUserViewSet, basename='attendance-user')
router.register(r'requests', AttendanceRequestViewSet, basename='attendance-request')
router.register(r'', AttendanceViewSet, basename='attendance')

urlpatterns = [
    # path("", include((router.urls, "attendance"), namespace="attendance")),
]
