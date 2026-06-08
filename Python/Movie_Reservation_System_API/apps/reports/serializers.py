from rest_framework import serializers

class ReservationReportSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_email = serializers.EmailField()
    movie_title = serializers.CharField()
    cinema_name = serializers.CharField()
    showtime_starts_at = serializers.DateTimeField()
    seats_count = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2)
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

class RevenueReportSerializer(serializers.Serializer):
    movie_title = serializers.CharField()
    total_reservations = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)

class CapacityReportSerializer(serializers.Serializer):
    showtime_id = serializers.IntegerField()
    movie_title = serializers.CharField()
    cinema_name = serializers.CharField()
    starts_at = serializers.DateTimeField()
    total_seats = serializers.IntegerField()
    reserved_seats = serializers.IntegerField()
    available_seats = serializers.IntegerField()
    occupancy_percentage = serializers.FloatField()