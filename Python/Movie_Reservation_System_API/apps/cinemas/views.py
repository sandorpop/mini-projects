from .serializers import SeatSerializer, CinemaSerializer, CinemaDetailSerializer
from .models import Seat, Cinema
from rest_framework import viewsets, permissions
from ..users.permissions import IsAdmin

class CinemaViewSet(viewsets.ModelViewSet):
    queryset = Cinema.objects.prefetch_related('seats').all()
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CinemaDetailSerializer
        return CinemaSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]

class SeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = [permissions.IsAuthenticated]