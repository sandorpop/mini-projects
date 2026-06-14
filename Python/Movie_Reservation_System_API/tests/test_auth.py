import pytest
from apps.users.models import User

@pytest.mark.django_db
def test_register_success(api_client):
    res = api_client.post('/auth/register/', {'email': 'newuser@test.com', 'full_name': 'New User', 'password': 'testpass123'})
    
    assert res.status_code == 201
    assert res.data['email'] == 'newuser@test.com'
    assert 'password' not in res.data
    assert User.objects.filter(email='newuser@test.com').exists()

@pytest.mark.django_db
def test_register_duplicate_email(api_client, regular_user):
    res = api_client.post('/auth/register/', {'email': 'user@test.com', 'full_name': 'Duplicate', 'password': 'testpass123'})
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_register_invalid_email(api_client):
    res = api_client.post('/auth/register/', {'email': 'notanemail', 'full_name': 'Test', 'password': 'testpass123'})
    
    assert res.status_code == 400

@pytest.mark.django_db
def test_login_success(api_client, regular_user):
    res = api_client.post('/auth/login/', {'email': 'user@test.com', 'password': 'testpass123'})
    
    assert res.status_code == 200
    assert 'access' in res.data
    assert 'refresh' in res.data

@pytest.mark.django_db
def test_login_wrong_password(api_client, regular_user):
    res = api_client.post('/auth/login/', {'email': 'user@test.com', 'password': 'wrongpassword'})
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_login_wrong_email(api_client):
    res = api_client.post('/auth/login/', {'email': 'nonexistent@test.com', 'password': 'testpass123'})
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_logout_success(api_client, regular_user):
    login_res = api_client.post('/auth/login/', {'email': 'user@test.com', 'password': 'testpass123'})
    refresh_token = login_res.data['refresh']
    
    res = api_client.post('/auth/logout/', {'refresh': refresh_token})
    
    assert res.status_code == 200

@pytest.mark.django_db
def test_logout_invalid_token(api_client):
    res = api_client.post('/auth/logout/', {'refresh': 'invalidtoken'})
    
    assert res.status_code == 401

@pytest.mark.django_db
def test_token_refresh_success(api_client, regular_user):
    login_res = api_client.post('/auth/login/', {'email': 'user@test.com', 'password': 'testpass123'})
    refresh_token = login_res.data['refresh']
    
    res = api_client.post('/auth/token/refresh/', {'refresh': refresh_token})
    
    assert res.status_code == 200
    assert 'access' in res.data

@pytest.mark.django_db
def test_token_refresh_blacklisted(api_client, regular_user):
    login_res = api_client.post('/auth/login/', {'email': 'user@test.com', 'password': 'testpass123'})
    refresh_token = login_res.data['refresh']
    
    api_client.post('/auth/logout/', {'refresh': refresh_token})
    
    res = api_client.post('/auth/token/refresh/', {'refresh': refresh_token})
    
    assert res.status_code == 401
