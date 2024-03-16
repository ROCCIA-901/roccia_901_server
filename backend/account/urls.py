from django.urls import path

from .views import (
    CustomTokenRefreshAPIView,
    PasswordUpdateAuthCodeValidationAPIView,
    PasswordUpdateRequestAuthCodeAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    UserPasswordUpdateAPIView,
    UserRegisterAuthCodeValidationAPIView,
    UserRegisterRequestAuthCodeAPIView,
    UserRegistrationAPIView,
)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("user-register-auth-code-request/", UserRegisterRequestAuthCodeAPIView.as_view(),
         name="user-register-auth-code-request"),
    path("user-register-auth-code-verify/", UserRegisterAuthCodeValidationAPIView.as_view(),
         name="user-register-auth-code-verify"),
    path("password-update-auth-code-request/", PasswordUpdateRequestAuthCodeAPIView.as_view(),
         name="password-update-auth-code-request"),
    path("password-update-auth-code-verify/", PasswordUpdateAuthCodeValidationAPIView.as_view(),
         name="password-update-auth-code-verify"),
    path("token-refresh/", CustomTokenRefreshAPIView.as_view(), name="token-refresh"),
    path('logout/', UserLogoutAPIView.as_view(), name='logout'),
    path('password-update/', UserPasswordUpdateAPIView.as_view(), name='logout'),
]
