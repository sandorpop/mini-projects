import pytest
from apps.reservations.models import Reservation

@pytest.mark.django_db
def test_create_reservation_success(user_client, showtime, seats):
    data = {'showtime': showtime.id, 'seat_ids': [seats[0].id, seats[1].id]}
    res = user_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 201
    assert float(res.data['total_price']) == (showtime.price * len(data['seat_ids']))
    assert res.data['status'] == Reservation.CONFIRMED

@pytest.mark.django_db
def test_create_reservation_unauthenticated(api_client, showtime, seats):
    data = {'showtime': showtime.id, 'seat_ids': [seats[0].id, seats[1].id]}
    res = api_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_create_reservation_past_showtime(user_client, past_showtime, seats):
    data = {'showtime': past_showtime.id, 'seat_ids': [seats[0].id, seats[1].id]}
    res = user_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_create_reservation_invalid_seats(user_client, showtime):
    data = {'showtime': showtime.id, 'seat_ids': [88888, 88889]}
    res = user_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_create_reservation_already_reserved(user_client, showtime, seats, reservation):
    data = {'showtime': showtime.id, 'seat_ids': [seats[0].id, seats[1].id]}
    res = user_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 400
    
@pytest.mark.django_db
def test_create_reservation_empty_seat_ids(user_client, showtime, seats):
    data = {'showtime': showtime.id, 'seat_ids': []}
    res = user_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_create_reservation_non_existent_showtime(user_client, seats):
    data = {'showtime': 88888, 'seat_ids': [seats[0].id, seats[1].id]}
    res = user_client.post('/reservations/', data=data, format='json')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_list_reservations_own_only(user_client, reservation, admin_reservation):
    res = user_client.get('/reservations/')
    
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]['id'] == reservation.id

@pytest.mark.django_db
def test_list_reservations_admin_sees_all(admin_client, reservation, admin_reservation):
    res = admin_client.get('/reservations/')
    
    assert res.status_code == 200
    assert len(res.data) == 2

@pytest.mark.django_db
def test_retrieve_reservation_own(user_client, reservation):
    res = user_client.get(f'/reservations/{reservation.id}/')
    
    assert res.status_code == 200
    assert res.data['id'] == reservation.id

@pytest.mark.django_db
def test_retrieve_reservation_unauthenticated(api_client, reservation):
    res = api_client.get(f'/reservations/{reservation.id}/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_retrieve_other_user_reservation(user_client, admin_reservation):
    res = user_client.get(f'/reservations/{admin_reservation.id}/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_retrieve_non_existent_reservation(user_client):
    res = user_client.get('/reservations/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_cancel_reservation_success(user_client, reservation):
    res = user_client.patch(f'/reservations/{reservation.id}/cancel/')
    
    assert res.status_code == 200
    assert res.data['status'] == Reservation.CANCELLED

@pytest.mark.django_db
def test_cancel_reservation_already_cancelled(user_client, reservation):
    first_cancel_res = user_client.patch(f'/reservations/{reservation.id}/cancel/')
    
    assert first_cancel_res.status_code == 200
    
    second_cancel_res = user_client.patch(f'/reservations/{reservation.id}/cancel/')
    
    assert second_cancel_res.status_code == 400

@pytest.mark.django_db
def test_cancel_past_reservation(user_client, past_reservation):
    res = user_client.patch(f'/reservations/{past_reservation.id}/cancel/')
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_cancel_other_user_reservation(user_client, admin_reservation):
    res = user_client.patch(f'/reservations/{admin_reservation.id}/cancel/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_cancel_unauthenticated(api_client, reservation):
    res = api_client.patch(f'/reservations/{reservation.id}/cancel/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_cancel_non_existent_reservation(user_client):
    res = user_client.patch('/reservations/88888/cancel/')
    
    assert res.status_code == 404