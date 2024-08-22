# mypy: ignore-errors

from django.urls import path

from attendance.views import AttendanceAPIView, AttendanceLocationAPIView

urlpatterns = [
    path("location/", AttendanceLocationAPIView.as_view(), name="location"),
    path("", AttendanceAPIView.as_view(), name="attendance"),
]
