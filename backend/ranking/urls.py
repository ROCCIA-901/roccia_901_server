from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ranking.views import RankingViewSet

router = DefaultRouter()
router.register(r'', RankingViewSet, basename='rankings')

urlpatterns = [
    path("weeks/", include((router.urls, "ranking"), namespace="rankings")),
]
