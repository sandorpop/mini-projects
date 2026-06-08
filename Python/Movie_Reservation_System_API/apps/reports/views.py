from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Sum, F
from apps.reservations.models import Reservation, ReservationSeat
from apps.showtimes.models import Showtime
from .serializers import ReservationReportSerializer, RevenueReportSerializer, CapacityReportSerializer
from apps.users.permissions import IsAdmin

class ReservationReportView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        queryset = Reservation.objects.select_related('user', 'showtime__movie', 'showtime__cinema').prefetch_related('seats')
        
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')
        movie_id = request.query_params.get('movie')
        
        if from_date:
            queryset = queryset.filter(showtime__starts_at__date__gte=from_date)
        if to_date:
            queryset = queryset.filter(showtime__starts_at__date__lte=to_date)
        if movie_id:
            queryset = queryset.filter(showtime__movie_id=movie_id)
        
        data = [
            {
                'id': r.id,
                'user_email': r.user.email,
                'movie_title': r.showtime.movie.title,
                'cinema_name': r.showtime.cinema.name,
                'showtime_starts_at': r.showtime.starts_at,
                'seats_count': r.seats.count(),
                'total_price': r.total_price,
                'status': r.status,
                'created_at': r.created_at
            }
            for r in queryset
        ]
        
        serializer = ReservationReportSerializer(data, many=True)
        return Response(serializer.data)

class RevenueReportView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        revenue_data = Reservation.objects.filter(
            status='confirmed'
        ).values(
            movie_title=F('showtime__movie__title')
        ).annotate(
            total_reservations=Count('id'),
            total_revenue=Sum('total_price')
        ).order_by('-total_revenue')
        
        serializer = RevenueReportSerializer(revenue_data, many=True)
        
        return Response(serializer.data)
    
class CapacityReportView(APIView):
    permission_classes = [IsAdmin]
    
    def get(self, request):
        showtimes = Showtime.objects.select_related('movie', 'cinema')
        
        date = request.query_params.get('date')
        if date:
            showtimes = showtimes.filter(starts_at__date=date)
        
        data = []
        for showtime in showtimes:
            reserved = ReservationSeat.objects.filter(showtime=showtime, reservation__status='confirmed').count()
            total = showtime.cinema.total_seats
            available = total - reserved
            occupancy = round((reserved / total * 100), 2) if total > 0 else 0
            
            data.append({
                'showtime_id': showtime.id,
                'movie_title': showtime.movie.title,
                'cinema_name': showtime.cinema.name,
                'starts_at': showtime.starts_at,
                'total_seats': total,
                'reserved_seats': reserved,
                'available_seats': available,
                'occupancy_percentage': occupancy
            })
        
        serializer = CapacityReportSerializer(data, many=True)
        
        return Response(serializer.data)