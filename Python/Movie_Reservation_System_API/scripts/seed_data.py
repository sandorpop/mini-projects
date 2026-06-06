import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_reservation_system.settings')
django.setup()

from apps.users.models import User, Role
from apps.movies.models import Genre
from apps.cinemas.models import Cinema

def seed_genres():
    genres = [
        'Action',
        'Adventure',
        'Animation',
        'Comedy',
        'Crime',
        'Documentary',
        'Drama',
        'Family',
        'Fantasy',
        'History',
        'Horror',
        'Music',
        'Mystery',
        'Romance',
        'Science Fiction',
        'TV Movie',
        'Thriller',
        'War',
        'Western'
    ]
    for name in genres:
        Genre.objects.get_or_create(name=name)
    print(f"Seeded {len(genres)} genres.")

def seed_admin():
    if not User.objects.filter(role=Role.ADMIN).exists():
        User.objects.create_superuser(
            username='admin@cinema.com',
            email='admin@cinema.com',
            full_name='System Admin',
            password='admin123',
            role=Role.ADMIN
        )
        print("Admin user created.")
    else:
        print("Admin already exists, skipping.")

def seed_cinema():
    if not Cinema.objects.filter(name="Cinema City").exists():
        cinema = Cinema.objects.create(name="Cinema City", total_seats=100)
        cinema.generate_seats()
        print("Cinema seeded.")
    else:
        print("Cinema already exists, skipping.")

if __name__ == '__main__':
    seed_genres()
    seed_admin()
    seed_cinema()