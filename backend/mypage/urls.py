from django.urls import path

from mypage.views import MypageAPIView

urlpatterns = [
    path("", MypageAPIView.as_view(), name="mypage"),
]
