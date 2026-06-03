from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def root(request):
    return JsonResponse({"message": "Movie Reservation API"})

urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls')),
    path('movies/', include('apps.movies.urls')),
    path('cinemas/', include('apps.cinemas.urls')),
    path('showtimes/', include('apps.showtimes.urls')),
    path('reservations/', include('apps.reservations.urls')),
    path('reports/', include('apps.reports.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)