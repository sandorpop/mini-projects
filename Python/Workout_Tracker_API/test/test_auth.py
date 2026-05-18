import pytest
from src.schemas import auth
from src.config import settings
from jose import jwt

def test_create_user(client):
    res = client.post("/auth/register", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = auth.UserOut(**res.json())
    
    assert res.status_code == 201
    assert new_user.email == "hello123@gmail.com"
    
def test_login_user(client, test_user):
    res = client.post("/auth/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = auth.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('arnold@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('arnold@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/auth/login", data={"username": email, "password": password})
    
    assert res.status_code == status_code

