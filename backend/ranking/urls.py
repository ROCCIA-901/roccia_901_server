from django.urls import path
from rest_framework.routers import DefaultRouter

from ranking.views import WeeklyRankingViewSet, get_generation_rankings

router = DefaultRouter()
router.register(r"weeks", WeeklyRankingViewSet, basename="weekly_rankings")

urlpatterns = router.urls + [
    path("generations/", get_generation_rankings, name="generation_rankings"),
]
