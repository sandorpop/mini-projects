from rest_framework import viewsets, permissions
from .serializers import GenreSerializer, MovieSerializer, MovieDetailSerializer
from .models import Genre, Movie
from ..users.permissions import IsAdmin

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.prefetch_related('genre').all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return MovieDetailSerializer
        return MovieSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]