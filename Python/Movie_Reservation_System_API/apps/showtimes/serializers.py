from rest_framework import serializers
from .models import Showtime
from ..movies.models import Movie
from ..cinemas.models import Cinema
from ..movies.serializers import MovieSerializer
from ..cinemas.serializers import CinemaSerializer
from ..reservations.models import ReservationSeat

def calculate_available_seats(obj):
    reserved_seats = ReservationSeat.objects.filter(showtime=obj, reservation__status='confirmed').count()
    
    return obj.cinema.total_seats - reserved_seats

class ShowtimeSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    cinema = serializers.PrimaryKeyRelatedField(queryset=Cinema.objects.all())
    
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'cinema', 'starts_at', 'ends_at', 'price', 'created_at']
    
    def validate(self, attrs):
        starts_at  = attrs.get('starts_at')
        ends_at = attrs.get('ends_at')
        cinema = attrs.get('cinema')
        
        if self.instance:
            starts_at = starts_at or self.instance.starts_at
            ends_at = ends_at or self.instance.ends_at
            cinema = cinema or self.instance.cinema
            
        if starts_at >= ends_at:
            raise serializers.ValidationError("Start time must be before end time.")
        
        overlapping_showtimes = Showtime.objects.filter(cinema=cinema, starts_at__lt=ends_at, ends_at__gt=starts_at)
        
        if self.instance:
            overlapping_showtimes = overlapping_showtimes.exclude(pk=self.instance.pk)
            
        if overlapping_showtimes.exists():
            raise serializers.ValidationError("This showtime overlaps with an existing showtime in the same cinema.")
        
        return attrs
class ShowtimeDetailSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    cinema = CinemaSerializer(read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'cinema', 'starts_at', 'ends_at', 'price', 'created_at', 'available_seats']
    
    def get_available_seats(self, obj):
        return calculate_available_seats(obj)
    
class ShowtimeListSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    cinema = CinemaSerializer(read_only=True)
    available_seats = serializers.SerializerMethodField()
    
    class Meta:
        model = Showtime
        fields = ['id', 'movie', 'cinema', 'starts_at', 'ends_at', 'price', 'available_seats']
    
    def get_available_seats(self, obj):
        return calculate_available_seats(obj)