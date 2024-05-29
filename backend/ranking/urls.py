from django.urls import path

from ranking.views import get_generation_rankings, get_weekly_rankings

urlpatterns = [
    path("weeks/", get_weekly_rankings, name="weekly_rankings"),
    path("generations/", get_generation_rankings, name="generation_rankings"),
]
