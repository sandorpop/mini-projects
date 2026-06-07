from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ShowtimeViewSet

router = DefaultRouter()
router.register('', ShowtimeViewSet)

urlpatterns = router.urls