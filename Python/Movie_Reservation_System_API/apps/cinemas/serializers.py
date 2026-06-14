from rest_framework import serializers
from .models import Cinema, Seat

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'number']
        read_only_fields = ['id', 'row', 'number']

class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'total_seats']
    
    def create(self, validated_data):
        cinema = Cinema.objects.create(**validated_data)
        cinema.generate_seats()
        return cinema

class CinemaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'total_seats']
        read_only_fields = ['total_seats']

class CinemaDetailSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cinema
        fields = ['id', 'name', 'total_seats', 'seats']