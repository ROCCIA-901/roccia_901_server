from django.urls import path

from .views import UserLoginAPIView, UserRegistrationAPIView

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="register"),
    path("login/", UserLoginAPIView.as_view(), name="login"),
]
