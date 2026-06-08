from rest_framework import viewsets, permissions, status
from .serializers import ReservationSerializer, ReservationStatusSerializer, ReservationDetailSerializer
from .models import Reservation, ReservationSeat
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    
    def get_queryset(self):
        user = self.request.user
        queryset = Reservation.objects.select_related(
            'showtime__movie',
            'showtime__cinema'
        ).prefetch_related('seats__seat')
        
        if user.role == 'admin':
            return queryset
        return queryset.filter(user=user)
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReservationDetailSerializer
        if self.action == 'partial_update':
            return ReservationStatusSerializer
        return ReservationSerializer
    
    def perform_create(self, serializer):
        serializer.save()
    
    @action(detail=True, methods=['patch'], url_path='cancel')
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        
        if reservation.user != request.user:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
            
        if reservation.status == Reservation.CANCELLED:
            return Response({'detail': 'Already cancelled.'}, status=status.HTTP_400_BAD_REQUEST)
            
        if reservation.showtime.starts_at <= timezone.now():
            return Response({'detail': 'Cannot cancel past or ongoing reservations.'}, status=status.HTTP_400_BAD_REQUEST)
            
        reservation.status = Reservation.CANCELLED
        reservation.save()
        
        return Response(ReservationDetailSerializer(reservation).data)