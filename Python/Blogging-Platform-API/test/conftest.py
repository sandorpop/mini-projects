import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from src.config import settings
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import Base, get_db
from src.oauth2 import create_access_token
from src import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    
@pytest.fixture()
def test_user(client):
    user_data = {"email": "mike@gmail.com", "password": "password123"}
    res = client.post("/register", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {"email": "steven@gmail.com", "password": "password123"}
    res = client.post("/register", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "1st title",
            "content": "1st content",
            "category": "Technology",
            "tags": ["Tech", "Programming"],
            "owner_id": test_user['id']
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "category": "Technology",
            "tags": ["Tech", "Programming"],
            "owner_id": test_user['id']
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "category": "Fashion",
            "tags": ["Dress", "Paris"],
            "owner_id": test_user['id']
        },
        {
            "title": "4th title",
            "content": "4th content",
            "category": "Technology",
            "tags": ["Tech", "Programming"],
            "owner_id": test_user2['id']
        }
    ]
        
    post_map = map(lambda post: models.Post(**post), posts_data)
    posts = list(post_map)
    
    session.add_all(posts)
    session.commit()
    
    posts = session.query(models.Post).all()
    
    return posts