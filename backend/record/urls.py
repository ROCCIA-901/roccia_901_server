from rest_framework.routers import DefaultRouter

from record.views import RecordViewSet

router = DefaultRouter()
router.register(r'', RecordViewSet, basename='records')

urlpatterns = router.urls
