import pytest
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, Role
from apps.movies.models import Movie, Genre
from apps.cinemas.models import Cinema, Seat
from apps.showtimes.models import Showtime
from apps.reservations.models import Reservation, ReservationSeat

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def regular_user(db):
    return User.objects.create_user(
        email='user@test.com',
        full_name='Test User',
        password='testpass123'
    )

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        email='admin@test.com',
        full_name='Admin User',
        password='testpass123',
        role=Role.ADMIN
    )

@pytest.fixture
def user_client(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def genre(db):
    return Genre.objects.create(name='Action')

@pytest.fixture
def movie(db, genre):
    m = Movie.objects.create(title='Test Movie', description='Test Description', duration=120)
    m.genre.add(genre)
    return m

@pytest.fixture
def cinema(db):
    c = Cinema.objects.create(name='Test Cinema', total_seats=60)
    c.generate_seats()
    return c

@pytest.fixture
def seats(cinema):
    return list(Seat.objects.filter(cinema=cinema)[:3])

@pytest.fixture
def showtime(db, movie, cinema):
    return Showtime.objects.create(
        movie=movie,
        cinema=cinema,
        starts_at=timezone.now() + timedelta(days=1),
        ends_at=timezone.now() + timedelta(days=1, hours=2),
        price=15.00
    )

@pytest.fixture
def past_showtime(db, movie, cinema):
    return Showtime.objects.create(
        movie=movie,
        cinema=cinema,
        starts_at=timezone.now() - timedelta(days=1),
        ends_at=timezone.now() - timedelta(hours=22),
        price=15.00
    )

@pytest.fixture
def reservation(db, regular_user, showtime, seats):
    r = Reservation.objects.create(
        user=regular_user,
        showtime=showtime,
        total_price=len(seats) * showtime.price,
        status='confirmed'
    )
    ReservationSeat.objects.bulk_create([
        ReservationSeat(reservation=r, seat=s, showtime=showtime)
        for s in seats
    ])
    return r

@pytest.fixture
def admin_reservation(db, admin_user, showtime, seats):
    admin_seats = list(Seat.objects.filter(cinema=showtime.cinema)[3:5])
    r = Reservation.objects.create(
        user=admin_user,
        showtime=showtime,
        total_price=len(admin_seats) * showtime.price,
        status='confirmed'
    )
    ReservationSeat.objects.bulk_create([
        ReservationSeat(reservation=r, seat=s, showtime=showtime)
        for s in admin_seats
    ])
    return r

@pytest.fixture
def past_reservation(db, regular_user, past_showtime, seats):
    r = Reservation.objects.create(
        user=regular_user,
        showtime=past_showtime,
        total_price=len(seats) * past_showtime.price,
        status='confirmed'
    )
    ReservationSeat.objects.bulk_create([
        ReservationSeat(reservation=r, seat=s, showtime=past_showtime)
        for s in seats
    ])
    return r