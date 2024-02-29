from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import (
    AttendanceRequestViewSet,
    AttendanceUserViewSet,
    AttendanceViewSet,
)

router = DefaultRouter()
router.register(r'', AttendanceViewSet, basename='attendance')
router.register(r'requests', AttendanceRequestViewSet, basename='attendance-request')
router.register(r'users', AttendanceUserViewSet, basename='attendance-user')

urlpatterns = [
    path("", include((router.urls, "attendance"), namespace="attendance")),
]
