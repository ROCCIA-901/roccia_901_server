# mypy: ignore-errors

from django.urls import path

from attendance.views import (
    AttendanceAcceptAPIView,
    AttendanceAPIView,
    AttendanceLocationAPIView,
    AttendanceRejectAPIView,
)

urlpatterns = [
    path("location/", AttendanceLocationAPIView.as_view(), name="location"),
    path("", AttendanceAPIView.as_view(), name="attendance"),
    path("requests/<int:attendance_id>/accept/", AttendanceAcceptAPIView.as_view(), name="attendance-accept"),
    path("requests/<int:attendance_id>/reject/", AttendanceRejectAPIView.as_view(), name="attendance-reject"),
]
