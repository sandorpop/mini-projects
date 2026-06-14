import pytest

@pytest.mark.django_db
def test_reservation_report_admin(admin_client, reservation, past_reservation, cinema, movie, regular_user):
    res = admin_client.get('/reports/reservations/')
    
    assert res.status_code == 200
    assert len(res.data) == 2
    assert res.data[0]['user_email'] == regular_user.email
    assert res.data[0]['movie_title'] == movie.title
    assert res.data[0]['cinema_name'] == cinema.name

@pytest.mark.django_db
def test_reservation_report_unauthorized(user_client):
    res = user_client.get('/reports/reservations/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_reservation_report_unauthenticated(api_client):
    res = api_client.get('/reports/reservations/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_reservation_report_filter_by_date(admin_client, reservation, past_reservation):
    date = reservation.showtime.starts_at.date()
    res = admin_client.get('/reports/reservations/', {'from_date': date,'to_date': date})
    
    assert res.status_code == 200
    assert len(res.data) == 1

@pytest.mark.django_db
def test_reservation_report_filter_by_movie(admin_client, reservation, past_reservation, movie):
    res = admin_client.get('/reports/reservations/', {'movie': movie.id})
    
    assert res.status_code == 200
    assert len(res.data) == 2

@pytest.mark.django_db
def test_reservation_report_empty(admin_client):
    res = admin_client.get('/reports/reservations/')
    
    assert res.status_code == 200
    assert len(res.data) == 0

@pytest.mark.django_db
def test_revenue_report_admin(admin_client, reservation, past_reservation):
    res = admin_client.get('/reports/revenue/')
    
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]['movie_title'] == reservation.showtime.movie.title
    assert float(res.data[0]['total_revenue']) == reservation.total_price + past_reservation.total_price

@pytest.mark.django_db
def test_revenue_report_unauthorized(user_client):
    res = user_client.get('/reports/revenue/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_revenue_report_unauthenticated(api_client):
    res = api_client.get('/reports/revenue/')
    
    assert res.status_code == 401
    
@pytest.mark.django_db
def test_revenue_report_empty(admin_client):
    res = admin_client.get('/reports/revenue/')
    
    assert res.status_code == 200
    assert len(res.data) == 0

@pytest.mark.django_db
def test_capacity_report_admin(admin_client, reservation, past_reservation, seats):
    res = admin_client.get('/reports/capacity/')
    assert res.status_code == 200
    assert len(res.data) == 2
    
    future_entry = next(
        r for r in res.data 
        if r['showtime_id'] == reservation.showtime.id
    )
    assert future_entry['total_seats'] == reservation.showtime.cinema.total_seats
    assert future_entry['reserved_seats'] == len(seats)
    assert future_entry['occupancy_percentage'] == round(len(seats) / reservation.showtime.cinema.total_seats * 100, 2)

@pytest.mark.django_db
def test_capacity_report_unauthorized(user_client):
    res = user_client.get('/reports/capacity/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_capacity_report_unauthenticated(api_client):
    res = api_client.get('/reports/capacity/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_capacity_report_filter_by_date(admin_client, reservation, past_reservation):
    date = reservation.showtime.starts_at.date()
    res = admin_client.get('/reports/capacity/', {'date': date})
    
    assert res.status_code == 200
    assert len(res.data) == 1

@pytest.mark.django_db
def test_capacity_report_empty(admin_client):
    res = admin_client.get('/reports/capacity/')
    
    assert res.status_code == 200
    assert len(res.data) == 0