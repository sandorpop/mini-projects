import pytest
from src.schemas import exercise
from src.models import Category, MuscleGroup, Exercise

def test_get_all_exercises(authorized_client, test_exercises):
    res = authorized_client.get("/exercises/")
    exercises_map = map(lambda ex: exercise.ExerciseOut(**ex), res.json())
    exercises_list = list(exercises_map)
    
    assert res.status_code == 200
    assert len(res.json()) == len(test_exercises)
    assert exercises_list[0].id == test_exercises[0].id

def test_get_exercises_with_category(authorized_client, test_exercises):
    res = authorized_client.get("/exercises/?category=strength")
    
    assert res.status_code == 200
    assert len(res.json()) == 4 # 4 exercises have STRENGTH category

def test_get_exercises_with_muscle_group(authorized_client, test_exercises):
    res = authorized_client.get("/exercises/?muscle_group=chest")
    
    assert res.status_code == 200
    assert len(res.json()) == 2 # 2 exercises have CHEST muscle group

def test_unauthorized_user_get_all_exercises(client, test_exercises):
    res = client.get("/exercises/")
    
    assert res.status_code == 200
    
def test_unauthorized_user_get_one_exercise(client, test_exercises):
    res = client.get(f"/exercises/{test_exercises[0].id}")
    
    assert res.status_code == 200
    
def test_get_unexistent_exercise(authorized_client, test_exercises):
    res = authorized_client.get(f"/exercises/88888888")
    
    assert res.status_code == 404

def test_get_one_exercise(authorized_client, test_exercises):
    res = authorized_client.get(f"/exercises/{test_exercises[0].id}")
    ex = exercise.ExerciseOut(**res.json())
    
    assert ex.id == test_exercises[0].id
    assert ex.description == test_exercises[0].description
    assert ex.category == test_exercises[0].category
    assert ex.muscle_group == test_exercises[0].muscle_group
    assert ex.is_seeded == test_exercises[0].is_seeded
    
@pytest.mark.parametrize("name, description, category, muscle_group", [
    ("Diamond Push Up", "Narrow push ups focusing on chest and triceps", "strength", "chest"),
    ("Hollow Body Hold", "Static exercise focusing on abdominal muscles, lying down while holding a posterior pelvic tilt", "flexibility", "core"),
    ("Calf Raises", "Motion done by ankles, focusing on calf muscles. Slow eccentric movements, standing on tiptoes and back to starting position.", "strength", "legs"),
])
def test_create_exercise(authorized_client, test_user, test_exercises, name, description, category, muscle_group):
    res = authorized_client.post("/exercises/", json={"name": name, "description": description, "category": category, "muscle_group": muscle_group})
    
    created_exercise = exercise.ExerciseOut(**res.json())
    
    assert res.status_code == 201
    assert created_exercise.name == name
    assert created_exercise.description == description
    assert created_exercise.category.value == category
    assert created_exercise.muscle_group.value == muscle_group
    assert created_exercise.created_by == test_user['id']
    assert created_exercise.is_seeded == False

def test_unauthorized_user_create_exercise(client, test_exercises, test_user):
    res = client.post("/exercises/", json={"name": "name", "description": "description", "category": "flexibility", "muscle_group": "legs"})
    
    assert res.status_code == 401
    
def test_unauthorized_user_delete_exercise(client, test_user, test_exercises):
    res = client.delete(f"/exercises/{test_exercises[0].id}")
    
    assert res.status_code == 401
    
def test_delete_exercise_success(authorized_client, test_user, session):
    custom_exercise = Exercise(name="Custom Exercise", 
                               description="A custom exercise", 
                               category=Category.STRENGTH, 
                               muscle_group=MuscleGroup.CHEST, 
                               is_seeded=False, 
                               created_by=test_user['id'])
    
    session.add(custom_exercise)
    session.commit()
    session.refresh(custom_exercise)
    
    res = authorized_client.delete(f"/exercises/{custom_exercise.id}")
    assert res.status_code == 204

def test_delete_other_user_exercise(authorized_client, test_user2, session):
    custom_exercise = Exercise(
        name="Other User Exercise",
        description="Belongs to user 2",
        category=Category.STRENGTH,
        muscle_group=MuscleGroup.BACK,
        is_seeded=False,
        created_by=test_user2['id']
    )
    session.add(custom_exercise)
    session.commit()
    session.refresh(custom_exercise)
    
    res = authorized_client.delete(f"/exercises/{custom_exercise.id}")
    assert res.status_code == 403

    
def test_delete_non_existent_exercise(authorized_client, test_user, test_exercises):
    res = authorized_client.delete(f"/exercises/8888888888888")
    
    assert res.status_code == 404

def test_delete_seeded_exercise(authorized_client, test_exercises, test_user):
    res = authorized_client.delete(f"/exercises/{test_exercises[0].id}")
    
    assert res.status_code == 403

def test_update_exercise(authorized_client, test_user, session):
    custom_exercise = Exercise(name="Custom Exercise", 
                               description="A custom exercise", 
                               category=Category.STRENGTH, 
                               muscle_group=MuscleGroup.CHEST, 
                               is_seeded=False, 
                               created_by=test_user['id'])
    
    session.add(custom_exercise)
    session.commit()
    session.refresh(custom_exercise)
    
    data = {
        "name": "updated name",
        "description": "updated description",
        "category": "cardio",
        "muscle_group": "core"
    }
    res = authorized_client.put(f"/exercises/{custom_exercise.id}", json=data)
    updated_exercise = exercise.ExerciseOut(**res.json())
    
    assert res.status_code == 200
    assert updated_exercise.name == data['name']
    assert updated_exercise.description == data['description']
    assert updated_exercise.category.value == data['category']
    assert updated_exercise.muscle_group.value == data['muscle_group']

def test_update_other_user_exercise(authorized_client, test_user2, session):
    custom_exercise = Exercise(
        name="Other User Exercise 2",
        description="Belongs to user 2",
        category=Category.STRENGTH,
        muscle_group=MuscleGroup.BACK,
        is_seeded=False,
        created_by=test_user2['id']
    )
    session.add(custom_exercise)
    session.commit()
    session.refresh(custom_exercise)
    
    data = {"name": "new name"}
    res = authorized_client.put(f"/exercises/{custom_exercise.id}", json=data)
    
    assert res.status_code == 403
    
def test_update_seeded_exercise(authorized_client, test_exercises):
    data = {
        "name": "updated name",
        "description": "updated description",
        "category": "cardio",
        "muscle_group": "core"
    }
    res = authorized_client.put(f"/exercises/{test_exercises[3].id}", json=data)
    
    assert res.status_code == 403

def test_update_non_existent_exercise(authorized_client, test_exercises):
    data = {
        "name": "updated name",
        "description": "updated description",
        "category": "cardio",
        "muscle_group": "core"
    }
    res = authorized_client.put(f"/exercises/888888888888", json=data)
    
    assert res.status_code == 404