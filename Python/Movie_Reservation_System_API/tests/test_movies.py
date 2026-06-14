import pytest
from apps.movies.models import Movie, Genre

@pytest.mark.django_db
def test_list_movies_public(api_client, movie, genre):
    res = api_client.get('/movies/')
    
    assert res.status_code == 200
    assert len(res.data) == 1
    assert res.data[0]['title'] == movie.title
    assert res.data[0]['duration'] == movie.duration
    assert res.data[0]['genre'][0]['name'] == genre.name

@pytest.mark.django_db
def test_retrieve_movie_public(api_client, movie):
    res = api_client.get(f'/movies/{movie.id}/')
    
    assert res.status_code == 200
    assert res.data['title'] == movie.title
    assert res.data['duration'] == movie.duration

@pytest.mark.django_db
def test_get_non_existent_movie(api_client):
    res = api_client.get('/movies/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_create_movie_admin(admin_client, genre):
    res = admin_client.post('/movies/', data={'title': 'Test Movie 2', 'description': 'Test description', 'duration': 140, 'genre': [genre.id]}, format='json')
    
    assert res.status_code == 201
    assert res.data['title'] == 'Test Movie 2'
    assert res.data['duration'] == 140
    assert Movie.objects.filter(title='Test Movie 2').exists()

@pytest.mark.django_db
def test_create_movie_unauthorized(user_client, genre):
    res = user_client.post('/movies/', data={'title': 'Test Movie 2', 'description': 'Test description', 'duration': 140, 'genre': [genre.id]}, format='json')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_create_movie_unauthenticated(api_client, genre):
    res = api_client.post('/movies/', data={'title': 'Test Movie 2', 'description': 'Test description', 'duration': 140, 'genre': [genre.id]}, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_update_movie_admin(admin_client, movie):
    data = {'title': 'Updated Title', 'description': 'Updated description', 'duration': 170}
    res = admin_client.patch(f'/movies/{movie.id}/', data=data, format='json')
    
    assert res.status_code == 200
    assert res.data['title'] == data['title']
    assert res.data['description'] == data['description']
    assert res.data['duration'] == data['duration']

@pytest.mark.django_db
def test_update_movie_unauthorized(user_client,movie):
    data = {'title': 'Updated Title', 'description': 'Updated description', 'duration': 170}
    res = user_client.patch(f'/movies/{movie.id}/', data=data, format='json')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_update_movie_unauthenticated(api_client, movie):
    data = {'title': 'Updated Title', 'description': 'Updated description', 'duration': 170}
    res = api_client.patch(f'/movies/{movie.id}/', data=data, format='json')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_update_non_existent_movie(admin_client):
    data = {'title': 'Updated Title', 'description': 'Updated description', 'duration': 170}
    res = admin_client.patch('/movies/888888/', data=data, format='json')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_delete_movie_admin(admin_client, movie):
    res = admin_client.delete(f'/movies/{movie.id}/')
    
    assert res.status_code == 204

@pytest.mark.django_db
def test_delete_movie_unauthorized(user_client, movie):
    res = user_client.delete(f'/movies/{movie.id}/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_delete_movie_unauthenticated(api_client, movie):
    res = api_client.delete(f'/movies/{movie.id}/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_delete_non_existent_movie(admin_client):
    res = admin_client.delete('/movies/88888/')
    
    assert res.status_code == 404

@pytest.mark.django_db
def test_list_genres_public(api_client, genre):
    res = api_client.get('/movies/genres/')
    
    assert res.status_code == 200
    assert res.data[0]['name'] == genre.name

@pytest.mark.django_db
def test_create_genre_admin(admin_client):
    res = admin_client.post('/movies/genres/', data={'name': 'Test Genre'})
    
    assert res.status_code == 201
    assert res.data['name'] == 'Test Genre'
    assert Genre.objects.filter(name='Test Genre').exists()

@pytest.mark.django_db
def test_create_genre_unauthorized(user_client):
    res = user_client.post('/movies/genres/', data={'name': 'Test Genre'})
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_create_genre_unauthenticated(api_client):
    res = api_client.post('/movies/genres/', data={'name': 'Test Genre'})
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_delete_genre_admin(admin_client, genre):
    res = admin_client.delete(f'/movies/genres/{genre.id}/')
    
    assert res.status_code == 204

@pytest.mark.django_db
def test_delete_genre_unauthorized(user_client, genre):
    res = user_client.delete(f'/movies/genres/{genre.id}/')
    
    assert res.status_code == 403

@pytest.mark.django_db
def test_delete_genre_unauthenticated(api_client, genre):
    res = api_client.delete(f'/movies/genres/{genre.id}/')
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_delete_non_existent_genre(admin_client):
    res = admin_client.delete('/movies/genres/8888/')
    
    assert res.status_code == 404