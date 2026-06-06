from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SeatViewSet, CinemaViewSet

router = DefaultRouter()
router.register('seats', SeatViewSet)
router.register('', CinemaViewSet)

urlpatterns = router.urls