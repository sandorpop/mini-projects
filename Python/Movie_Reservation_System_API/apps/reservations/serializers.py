from rest_framework import serializers
from .models import Reservation, ReservationSeat
from ..cinemas.serializers import SeatSerializer
from ..showtimes.serializers import ShowtimeListSerializer
from django.utils import timezone

class ReservationSeatSerializer(serializers.ModelSerializer):
    seat = SeatSerializer(read_only=True)
    
    class Meta:
        model = ReservationSeat
        fields = ['id', 'seat']

class ReservationSerializer(serializers.ModelSerializer):
    seat_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'showtime', 'seat_ids', 'total_price', 'status', 'created_at']
        read_only_fields = ['id', 'total_price', 'status', 'created_at']
    
    def validate(self, attrs):
        seats = attrs.get('seat_ids')
        showtime = attrs.get('showtime')
        
        if showtime.starts_at <= timezone.now():
            raise serializers.ValidationError("Cannot reserve seats for a past or ongoing showtime.")
        
        if not seats:
            raise serializers.ValidationError("You must select at least one seat.")
        
        from apps.cinemas.models import Seat
        valid_seats = Seat.objects.filter(id__in=seats, cinema=showtime.cinema)
        
        if valid_seats.count() != len(seats):
            raise serializers.ValidationError("One or more seats do not belong to this cinema.")
        
        already_reserved = ReservationSeat.objects.filter(showtime=showtime, seat_id__in=seats, reservation__status='confirmed').exists()
        if already_reserved:
            raise serializers.ValidationError("One or more seats are already reserved.")

        return attrs
    
    def create(self, validated_data):
        from django.db import transaction
        from apps.cinemas.models import Seat

        showtime = validated_data['showtime']
        seat_ids = validated_data['seat_ids']
        user = self.context['request'].user

        with transaction.atomic():
            # lock seats to prevent concurrent reservations
            Seat.objects.select_for_update().filter(id__in=seat_ids)

            # re-check availability inside the lock
            already_reserved = ReservationSeat.objects.filter(showtime=showtime, seat_id__in=seat_ids, reservation__status='confirmed').exists()

            if already_reserved:
                raise serializers.ValidationError("One or more seats were just reserved by someone else.")

            total_price = len(seat_ids) * showtime.price

            reservation = Reservation.objects.create(user=user, showtime=showtime, total_price=total_price, status=Reservation.CONFIRMED)

            ReservationSeat.objects.bulk_create([ReservationSeat(reservation=reservation, seat_id=seat_id, showtime=showtime) for seat_id in seat_ids])

            return reservation

class ReservationDetailSerializer(serializers.ModelSerializer):
    showtime = ShowtimeListSerializer(read_only=True)
    seats = ReservationSeatSerializer(many=True, read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'showtime', 'seats', 'total_price', 'status', 'created_at']

class ReservationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['status']