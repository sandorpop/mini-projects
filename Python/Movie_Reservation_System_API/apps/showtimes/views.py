from rest_framework import viewsets, permissions
from .serializers import ShowtimeSerializer, ShowtimeDetailSerializer, ShowtimeListSerializer
from .models import Showtime
from ..users.permissions import IsAdmin

class ShowtimeViewSet(viewsets.ModelViewSet):
    queryset = Showtime.objects.select_related('cinema','movie').all()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShowtimeDetailSerializer
        elif self.action == 'list':
            return ShowtimeListSerializer
        else:
            return ShowtimeSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]
    
    def get_queryset(self):
        queryset = Showtime.objects.select_related('movie', 'cinema')
        date = self.request.query_params.get('date')
        movie_id = self.request.query_params.get('movie')
        
        if date:
            queryset = queryset.filter(starts_at__date=date)
        if movie_id:
            queryset = queryset.filter(movie_id=movie_id)

        return queryset