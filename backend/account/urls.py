from django.urls import path

from .views import (
    AuthCodeValidationAPIView,
    RequestAuthCodeAPIView,
    UserLoginAPIView,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("auth-code-request/", RequestAuthCodeAPIView.as_view(), name="auth-code-request"),
    path("auth-code-verify/", AuthCodeValidationAPIView.as_view(), name="auth-code-request"),
]
