from django.urls import path

from attendance.views import (
    AttendanceAcceptAPIView,
    AttendanceAPIView,
    AttendanceDetailAPIView,
    AttendanceLocationAPIView,
    AttendanceRateAPIView,
    AttendanceRejectAPIView,
    AttendanceRequestListAPIView,
    AttendanceUserListAPIView,
)

urlpatterns = [
    path("", AttendanceAPIView.as_view(), name="attendance"),
    path("requests/", AttendanceRequestListAPIView.as_view(), name="attendance-request-list"),
    path("requests/<int:attendance_id>/accept/", AttendanceAcceptAPIView.as_view(), name="attendance-accept"),
    path("requests/<int:attendance_id>/reject/", AttendanceRejectAPIView.as_view(), name="attendance-reject"),
    path("rate/", AttendanceRateAPIView.as_view(), name="attendance-rate"),
    path("users/<int:user_id>/details/", AttendanceDetailAPIView.as_view(), name="attendance-detail"),
    path("location/", AttendanceLocationAPIView.as_view(), name="attendance-location"),
    path("users/", AttendanceUserListAPIView.as_view(), name="attendance-user-list"),
]
