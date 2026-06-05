from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, MovieViewSet

router = DefaultRouter()
router.register('genres', GenreViewSet)
router.register('', MovieViewSet)

urlpatterns = router.urls