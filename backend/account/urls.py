from django.urls import path

from .views import (
    AuthCodeValidationAPIView,
    CustomTokenRefreshAPIView,
    RequestAuthCodeAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserPasswordUpdateAPIView,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("auth-code-request/", RequestAuthCodeAPIView.as_view(), name="auth-code-request"),
    path("auth-code-verify/", AuthCodeValidationAPIView.as_view(), name="auth-code-verify"),
    path("token-refresh/", CustomTokenRefreshAPIView.as_view(), name="token-refresh"),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('password-update/', UserPasswordUpdateAPIView.as_view(), name='logout'),
]
