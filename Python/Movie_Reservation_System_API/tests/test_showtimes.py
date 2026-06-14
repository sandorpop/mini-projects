import pytest
from apps.showtimes.models import Showtime
from datetime import datetime, timezone, timedelta

@pytest.mark.django_db
def test_list_showtimes_public(api_client, showtime):
    res = api_client.get('/showtimes/')
    
    assert res.status_code == 200
    assert float(res.data[0]['price']) == showtime.price

@pytest.mark.django_db
def test_retrieve_showtime_public(api_client, showtime):
    res = api_client.get(f'/showtimes/{showtime.id}/')
    
    assert res.status_code == 200
    assert float(res.data['price']) == showtime.price

@pytest.mark.django_db
def test_get_non_existent_showtime(api_client):
    res = api_client.get('/showtimes/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_create_showtime_admin(admin_client, movie, cinema):
    start_date = datetime.now(timezone.utc) + timedelta(days=2)
    end_date = datetime.now(timezone.utc) + timedelta(days=2, hours=2)
    data = {"movie": movie.id, "cinema": cinema.id, "starts_at": start_date, "ends_at": end_date, "price": 12.99}
    res = admin_client.post('/showtimes/', data=data, format='json')
    
    assert res.status_code == 201
    assert res.data['movie'] == data['movie']
    assert res.data['cinema'] == data['cinema']
    assert float(res.data['price']) == data['price']
    assert Showtime.objects.filter(price=data['price']).exists()

@pytest.mark.django_db
def test_create_showtime_unauthorized(user_client, movie, cinema):
    start_date = datetime.now(timezone.utc) + timedelta(days=2)
    end_date = datetime.now(timezone.utc) + timedelta(days=2, hours=2)
    data = {"movie": movie.id, "cinema": cinema.id, "starts_at": start_date, "ends_at": end_date, "price": 12.99}
    res = user_client.post('/showtimes/', data=data, format='json')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_create_showtime_unauthenticated(api_client, movie, cinema):
    start_date = datetime.now(timezone.utc) + timedelta(days=2)
    end_date = datetime.now(timezone.utc) + timedelta(days=2, hours=2)
    data = {"movie": movie.id, "cinema": cinema.id, "starts_at": start_date, "ends_at": end_date, "price": 12.99}
    res = api_client.post('/showtimes/', data=data, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_create_showtime_overlap(admin_client, movie, cinema, showtime):
    start_date = showtime.starts_at
    end_date = showtime.ends_at
    data = {"movie": movie.id, "cinema": cinema.id, "starts_at": start_date, "ends_at": end_date, "price": 12.99}
    res = admin_client.post('/showtimes/', data=data, format='json')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_create_showtime_no_overlap(admin_client, movie, cinema, showtime):
    start_date = showtime.starts_at + timedelta(hours=4)
    end_date = start_date + timedelta(hours=2)
    data = {"movie": movie.id, "cinema": cinema.id, "starts_at": start_date, "ends_at": end_date, "price": 12.99}
    res = admin_client.post('/showtimes/', data=data, format='json')
    
    assert res.status_code == 201
    assert res.data['movie'] == data['movie']
    assert res.data['cinema'] == data['cinema']
    assert float(res.data['price']) == data['price']

@pytest.mark.django_db
def test_create_showtime_ends_at_before_starts_at(admin_client, movie, cinema, showtime):
    start_date = datetime.now(timezone.utc) + timedelta(days=2)
    end_date = start_date - timedelta(hours=2)
    data = {"movie": movie.id, "cinema": cinema.id, "starts_at": start_date, "ends_at": end_date, "price": 12.99}
    res = admin_client.post('/showtimes/', data=data, format='json')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_update_showtime_admin(admin_client, showtime):
    data = {"price": 25.99}
    res = admin_client.patch(f'/showtimes/{showtime.id}/', data=data, format='json')
    
    assert res.status_code == 200
    assert float(res.data['price']) == data['price']

@pytest.mark.django_db
def test_update_showtime_unauthorized(user_client, showtime):
    data = {"price": 25.99}
    res = user_client.patch(f'/showtimes/{showtime.id}/', data=data, format='json')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_update_showtime_unauthenticated(api_client, showtime):
    data = {"price": 25.99}
    res = api_client.patch(f'/showtimes/{showtime.id}/', data=data, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_update_non_existent_showtime(admin_client):
    data = {"price": 25.99}
    res = admin_client.patch('/showtimes/88888/', data=data, format='json')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_delete_showtime_admin(admin_client, showtime):
    res = admin_client.delete(f'/showtimes/{showtime.id}/')
    
    assert res.status_code == 204

@pytest.mark.django_db
def test_delete_showtime_unauthorized(user_client, showtime):
    res = user_client.delete(f'/showtimes/{showtime.id}/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_delete_showtime_unauthenticated(api_client, showtime):
    res = api_client.delete(f'/showtimes/{showtime.id}/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_delete_non_existent_showtime(admin_client):
    res = admin_client.delete('/showtimes/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_filter_showtimes_by_date(api_client, showtime):
    date = showtime.starts_at.date()
    res = api_client.get('/showtimes/', {'date': date})
    
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]['id'] == showtime.id

@pytest.mark.django_db
def test_filter_showtimes_by_movie(api_client, showtime, movie):
    res = api_client.get('/showtimes/', {'movie': movie.id})
    
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]['id'] == showtime.id

@pytest.mark.django_db
def test_available_seats_decreases_after_reservation(user_client, showtime, seats):
    res_before = user_client.get(f'/showtimes/{showtime.id}/')
    available_before = res_before.data['available_seats']
    
    data = {'showtime': showtime.id, 'seat_ids': [seats[0].id, seats[1].id]}
    res = user_client.post('/reservations/', data=data, format='json')
    assert res.status_code == 201
    
    res_after = user_client.get(f'/showtimes/{showtime.id}/')
    available_after = res_after.data['available_seats']
    
    assert available_after == available_before - len(data['seat_ids'])