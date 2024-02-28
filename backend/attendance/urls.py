from django.urls import include, path
from rest_framework.routers import DefaultRouter

from attendance.views import AttendanceRequestViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'', AttendanceViewSet, basename='attendance')
router.register(r'requests', AttendanceRequestViewSet, basename='attendance-request')

urlpatterns = [
    path("", include((router.urls, "attendance"), namespace="attendance")),
]
