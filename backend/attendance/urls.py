from django.urls import path

from attendance.views import AttendanceRequest

urlpatterns = [
    path("", AttendanceRequest.as_view(), name="attendance-request"),
]
