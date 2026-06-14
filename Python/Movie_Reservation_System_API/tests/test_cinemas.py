import pytest
from apps.cinemas.models import Cinema, Seat

@pytest.mark.django_db
def test_list_cinemas_public(api_client, cinema):
    res = api_client.get('/cinemas/')
    
    assert res.status_code == 200
    assert res.data[0]['name'] == cinema.name
    assert res.data[0]['total_seats'] == cinema.total_seats

@pytest.mark.django_db
def test_retrieve_cinema_with_seats(api_client, cinema, seats):
    res = api_client.get(f'/cinemas/{cinema.id}/')
    
    assert res.status_code == 200
    assert res.data['name'] == cinema.name
    assert res.data['total_seats'] == cinema.total_seats
    assert len(res.data['seats']) == cinema.total_seats

@pytest.mark.django_db
def test_get_non_existent_cinema(api_client):
    res = api_client.get('/cinemas/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_create_cinema_admin(admin_client):
    data = {'name': 'Test Cinema 2', 'total_seats': 75}
    res = admin_client.post('/cinemas/', data=data, format='json')
    created_seats = Seat.objects.count()
    
    assert res.status_code == 201
    assert res.data['name'] == data['name']
    assert res.data['total_seats'] == data['total_seats']
    assert Cinema.objects.filter(name=data['name']).exists()
    assert created_seats == data['total_seats']

@pytest.mark.django_db
def test_create_cinema_unauthorized(user_client):
    data = {'name': 'Test Cinema 2', 'total_seats': 75}
    res = user_client.post('/cinemas/', data=data, format='json')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_create_cinema_unauthenticated(api_client):
    data = {'name': 'Test Cinema 2', 'total_seats': 75}
    res = api_client.post('/cinemas/', data=data, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_update_cinema_admin(admin_client, cinema):
    data = {'name': 'Updated Cinema', 'total_seats': 70}
    old_total_seats = cinema.total_seats
    res = admin_client.patch(f'/cinemas/{cinema.id}/', data=data, format='json')
    
    assert res.status_code == 200
    assert res.data['name'] == 'Updated Cinema'
    assert res.data['total_seats'] == old_total_seats

@pytest.mark.django_db
def test_update_cinema_unauthorized(user_client, cinema):
    data = {'name': 'Updated Cinema', 'total_seats': 70}
    res = user_client.patch(f'/cinemas/{cinema.id}/', data=data, format='json')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_update_cinema_unauthenticated(api_client, cinema):
    data = {'name': 'Updated Cinema', 'total_seats': 70}
    res = api_client.patch(f'/cinemas/{cinema.id}/', data=data, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_update_non_existent_cinema(admin_client):
    data = {'name': 'Updated Cinema', 'total_seats': 70}
    res = admin_client.patch('/cinemas/88888/', data=data, format='json')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_delete_cinema_admin(admin_client, cinema):
    res = admin_client.delete(f'/cinemas/{cinema.id}/')
    
    assert res.status_code == 204

@pytest.mark.django_db
def test_delete_cinema_unauthorized(user_client, cinema):
    res = user_client.delete(f'/cinemas/{cinema.id}/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_delete_cinema_unauthenticated(api_client, cinema):
    res = api_client.delete(f'/cinemas/{cinema.id}/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_delete_non_existent_cinema(admin_client):
    res = admin_client.delete('/cinemas/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_list_seats_authenticated(user_client, cinema, seats):
    res = user_client.get('/cinemas/seats/')
    
    assert res.status_code == 200
    assert len(res.data) == cinema.total_seats

@pytest.mark.django_db
def test_list_seats_unauthenticated(api_client, seats):
    res = api_client.get('/cinemas/seats/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_retrieve_seat_authenticated(user_client, cinema, seats):
    res = user_client.get(f'/cinemas/seats/{seats[0].id}/')
    
    assert res.status_code == 200
    assert res.data['row'] == seats[0].row
    assert res.data['number'] == seats[0].number

@pytest.mark.django_db
def test_retrieve_non_existent_seat(user_client):
    res = user_client.get('/cinemas/seats/88888/')
    
    assert res.status_code == 404