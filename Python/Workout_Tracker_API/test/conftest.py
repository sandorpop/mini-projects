import pytest
from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base, get_db
from src.main import app
from fastapi.testclient import TestClient
from src.oauth2 import create_access_token
from src import models
from datetime import datetime, timezone, timedelta


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
    user_data = {"email": "arnold@gmail.com", "password": "password123"}
    res = client.post("/auth/register", json=user_data)
    
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture()
def test_user2(client):
    user_data = {"email": "ronnie@gmail.com", "password": "password123"}
    res = client.post("/auth/register", json=user_data)
    
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
def test_exercises(session):
    exercises_data = [
        {"name": "Push Up", "description": "A basic push-up.", "category": models.Category.STRENGTH, "muscle_group": models.MuscleGroup.CHEST},
        {"name": "Squat", "description": "A basic squat.", "category": models.Category.STRENGTH, "muscle_group": models.MuscleGroup.LEGS},
        {"name": "Running", "description": "A basic running exercise.", "category": models.Category.CARDIO, "muscle_group": models.MuscleGroup.LEGS},
        {"name": "Plank", "description": "A basic plank.", "category": models.Category.FLEXIBILITY, "muscle_group": models.MuscleGroup.CORE},
        {"name": "Deadlift", "description": "A strength exercise targeting the lower back, hamstrings, and glutes.", "category": models.Category.STRENGTH, "muscle_group": models.MuscleGroup.BACK},
        {"name": "Bench Press", "description": "A compound exercise that targets the chest, shoulders, and triceps.", "category": models.Category.STRENGTH, "muscle_group": models.MuscleGroup.CHEST}
    ]
    
    exercise_map = map(lambda ex: models.Exercise(is_seeded=True, **ex), exercises_data)
    exercises = list(exercise_map)
    
    session.add_all(exercises)
    session.commit()
    
    exercises = session.query(models.Exercise).all()
    
    return exercises

@pytest.fixture
def test_workout(test_user, test_exercises, session):
    workout = models.Workout(
        title="Test Workout",
        description="Test Description",
        owner_id=test_user['id']
    )
    session.add(workout)
    session.flush()
    
    workout_exercises = [
        models.WorkoutExercise(workout_id=workout.id, exercise_id=test_exercises[0].id, sets=3, reps=10, weight_kg=None, order=1),
        models.WorkoutExercise(workout_id=workout.id, exercise_id=test_exercises[5].id, sets=4, reps=8, weight_kg=80.0, order=2)
    ]
    session.add_all(workout_exercises)
    session.commit()
    session.refresh(workout)
    return workout

@pytest.fixture
def test_workout2(test_user2, test_exercises, session):
    workout = models.Workout(
        title="Test Workout 2",
        description="Test Description 2",
        owner_id=test_user2['id']
    )
    session.add(workout)
    session.flush()
    
    workout_exercises = [
        models.WorkoutExercise(workout_id=workout.id, exercise_id=test_exercises[2].id, sets=3, reps=12, weight_kg=None, order=1)
    ]
    session.add_all(workout_exercises)
    session.commit()
    session.refresh(workout)
    return workout

@pytest.fixture
def test_scheduled_workout(test_workout, test_user, session):
    scheduled = models.ScheduledWorkout(
        workout_id=test_workout.id,
        user_id=test_user['id'],
        scheduled_at=datetime.now(timezone.utc) + timedelta(days=1),
        status=models.Status.PENDING
    )
    session.add(scheduled)
    session.commit()
    session.refresh(scheduled)
    return scheduled

@pytest.fixture
def test_scheduled_workout_active(test_workout, test_user, session):
    scheduled = models.ScheduledWorkout(
        workout_id=test_workout.id,
        user_id=test_user['id'],
        scheduled_at=datetime.now(timezone.utc) + timedelta(days=2),
        status=models.Status.ACTIVE
    )
    session.add(scheduled)
    session.commit()
    session.refresh(scheduled)
    session.expunge(scheduled)
    return scheduled

@pytest.fixture
def test_scheduled_workout2(test_workout2, test_user2, session):
    scheduled = models.ScheduledWorkout(
        workout_id=test_workout2.id,
        user_id=test_user2['id'],
        scheduled_at=datetime.now(timezone.utc) + timedelta(days=3),
        status=models.Status.PENDING
    )
    session.add(scheduled)
    session.commit()
    session.refresh(scheduled)
    return scheduled

@pytest.fixture
def test_log(test_scheduled_workout_active, test_user, session):
    log = models.WorkoutLog(
        scheduled_workout_id=test_scheduled_workout_active.id,
        user_id=test_user['id'],
        duration_minutes=45,
        notes="Felt great"
    )
    session.add(log)
    session.commit()
    session.refresh(log)
    return log

@pytest.fixture
def test_log_exercises(test_log, test_exercises, session):
    log_exercises = [
        models.WorkoutLogExercise(
            log_id=test_log.id,
            exercise_id=test_exercises[0].id,
            sets_completed=3,
            reps_completed=10,
            weight_used_kg=None
        ),
        models.WorkoutLogExercise(
            log_id=test_log.id,
            exercise_id=test_exercises[5].id,
            sets_completed=4,
            reps_completed=8,
            weight_used_kg=80.0
        )
    ]
    session.add_all(log_exercises)
    session.commit()
    for le in log_exercises:
        session.refresh(le)
    return log_exercises