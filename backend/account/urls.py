from django.urls import path

from .views import RequestAuthCodeAPIView, UserLoginAPIView, UserRegistrationAPIView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path("auth-code-request/", RequestAuthCodeAPIView.as_view(), name="auth-code-request"),
]
