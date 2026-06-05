from rest_framework import serializers
from .models import Genre, Movie

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.PrimaryKeyRelatedField(many=True, queryset=Genre.objects.all())
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'poster_image', 'genre', 'duration', 'created_at', 'updated_at']

class MovieDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'poster_image', 'genre', 'duration', 'created_at', 'updated_at']