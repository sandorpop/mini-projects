from src.schemas import workout
from src.models import Status, WorkoutLog, ScheduledWorkout
from datetime import date, datetime, timedelta, timezone

def test_create_workout(authorized_client, test_user, test_exercises):
    workout_data = {"title": "Chest Workout", "description": "Workout focusing on push exercises.", "exercises": [
        {"exercise_id": test_exercises[0].id, "sets": 4, "reps": 20, "order": 1},
        {"exercise_id": test_exercises[5].id, "sets": 4, "reps": 6, "weight_kg": 90.0, "order": 2}
    ]}
    
    res = authorized_client.post("/workouts/", json=workout_data)
    
    created_workout = workout.WorkoutOut(**res.json())
    
    assert res.status_code == 201
    assert created_workout.title == workout_data["title"]
    assert created_workout.description == workout_data["description"]
    assert len(created_workout.exercises) == 2
    assert created_workout.exercises[0].exercise_id == workout_data["exercises"][0]["exercise_id"]
    assert created_workout.exercises[1].exercise_id == workout_data["exercises"][1]["exercise_id"]
    assert created_workout.owner_id == test_user["id"]

def test_create_workout_unauthorized(client, test_exercises):
    res = client.post("/workouts/", json={"title": "title", "description": "description", "exercises": [{"exercise_id": test_exercises[1].id, "sets": 3, "reps": 6, "order": 1}]})
    
    assert res.status_code == 401
    
def test_get_all_workouts(authorized_client, test_workout):
    res = authorized_client.get("/workouts/")
    workouts_map = map(lambda wo: workout.WorkoutOut(**wo), res.json())
    workouts_list = list(workouts_map)
    
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert workouts_list[0].id == test_workout.id

def test_get_all_workouts_with_title_filter(authorized_client, test_workout):
    res = authorized_client.get("/workouts/?title=Test")
    
    assert res.status_code == 200
    assert len(res.json()) == 1

def test_get_all_workouts_unauthorized(client, test_workout):
    res = client.get("/workouts/")
    
    assert res.status_code == 401

def test_get_one_workout(authorized_client, test_workout):
    res = authorized_client.get(f"/workouts/{test_workout.id}")
    found_workout = workout.WorkoutOut(**res.json())
    
    assert res.status_code == 200
    assert found_workout.id == test_workout.id
    assert found_workout.title == test_workout.title
    assert found_workout.description == test_workout.description
    assert len(found_workout.exercises) == 2
    assert found_workout.exercises[0].id == test_workout.exercises[0].id
    assert found_workout.exercises[1].id == test_workout.exercises[1].id
    
def test_get_one_workout_unauthorized(client, test_workout):
    res = client.get(f"/workouts/{test_workout.id}")
    
    assert res.status_code == 401

def test_get_non_existent_workout(authorized_client):
    res = authorized_client.get("/workouts/88888888")
    
    assert res.status_code == 404

def test_get_other_user_workout(authorized_client, test_workout2):
    res = authorized_client.get(f"/workouts/{test_workout2.id}")
    
    assert res.status_code == 403

def test_update_workout(authorized_client, test_workout, test_exercises):
    workout_data = {"title": "updated title", "description": "updated description", "exercises": [{"exercise_id": test_exercises[3].id, "sets": 3, "reps": 6, "order": 1}]}
    res = authorized_client.put(f"/workouts/{test_workout.id}", json=workout_data)
    updated_workout = workout.WorkoutOut(**res.json())
    
    assert res.status_code == 200
    assert updated_workout.title == workout_data["title"]
    assert updated_workout.description == workout_data["description"]
    assert updated_workout.exercises[0].exercise_id == workout_data["exercises"][0]["exercise_id"]

def test_update_workout_unauthorized(client, test_workout):
    res = client.put(f"/workouts/{test_workout.id}", json={"title": "new title"})
    
    assert res.status_code == 401

def test_update_non_existent_workout(authorized_client):
    res = authorized_client.put(f"/workouts/888888", json={"title": "new title"})
    
    assert res.status_code == 404

def test_update_other_user_workout(authorized_client, test_workout2):
    res = authorized_client.put(f"/workouts/{test_workout2.id}", json={"title": "new title"})
    
    assert res.status_code == 403

def test_delete_workout_success(authorized_client, test_workout):
    res = authorized_client.delete(f"/workouts/{test_workout.id}")
    
    assert res.status_code == 204

def test_delete_workout_unauthorized(client, test_workout):
    res = client.delete(f"/workouts/{test_workout.id}")
    
    assert res.status_code == 401

def test_delete_non_existent_workout(authorized_client):
    res = authorized_client.delete("/workouts/888888")
    
    assert res.status_code == 404
    
def test_delete_other_user_workout(authorized_client, test_workout2):
    res = authorized_client.delete(f"/workouts/{test_workout2.id}")
    
    assert res.status_code == 403

def test_create_scheduled_workout(authorized_client, test_workout, test_user):
    res = authorized_client.post(f"/workouts/{test_workout.id}/schedule", json={"scheduled_at": "2026-05-20T10:00:00Z"})
    scheduled_workout = workout.ScheduledWorkoutOut(**res.json())
    
    assert res.status_code == 201
    assert scheduled_workout.scheduled_at.date() == date(2026, 5, 20)
    assert scheduled_workout.workout_id == test_workout.id
    assert scheduled_workout.user_id == test_user["id"]
    assert scheduled_workout.status == Status.PENDING

def test_schedule_workout_unauthorized(client, test_workout):
    res = client.post(f"/workouts/{test_workout.id}/schedule", json={"scheduled_at": "2026-05-24T7:00:00Z"})
    
    assert res.status_code == 401

def test_schedule_other_user_workout(authorized_client, test_workout2):
    res = authorized_client.post(f"/workouts/{test_workout2.id}/schedule", json={"scheduled_at": "2026-05-24T7:00:00Z"})
    
    assert res.status_code == 403

def test_get_scheduled_workouts(authorized_client, test_scheduled_workout):
    res = authorized_client.get("/workouts/scheduled/")
    scheduled_map = map(lambda sch: workout.ScheduledWorkoutOut(**sch), res.json())
    scheduled_list = list(scheduled_map)
    
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert scheduled_list[0].id == test_scheduled_workout.id

def test_get_scheduled_workouts_with_status_filter(authorized_client, test_scheduled_workout):
    res = authorized_client.get("/workouts/scheduled?status_filter=pending")
    scheduled_map = map(lambda sch: workout.ScheduledWorkoutOut(**sch), res.json())
    scheduled_list = list(scheduled_map)
    
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert scheduled_list[0].id == test_scheduled_workout.id
    assert scheduled_list[0].status == Status.PENDING

def test_get_scheduled_workouts_with_date_filter(authorized_client, test_scheduled_workout):
    to_date = datetime.now(timezone.utc) + timedelta(days=2)
    res = authorized_client.get("/workouts/scheduled", params={"from_date": "2026-05-10T07:00:00Z", "to_date": to_date})
    scheduled_map = map(lambda sch: workout.ScheduledWorkoutOut(**sch), res.json())
    scheduled_list = list(scheduled_map)
    
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert scheduled_list[0].id == test_scheduled_workout.id

def test_get_one_scheduled_workout(authorized_client, test_scheduled_workout, test_user, test_workout):
    res = authorized_client.get(f"/workouts/scheduled/{test_scheduled_workout.id}")
    found_scheduled = workout.ScheduledWorkoutOut(**res.json())
    
    assert res.status_code == 200
    assert found_scheduled.id == test_scheduled_workout.id
    assert found_scheduled.user_id == test_user["id"]
    assert found_scheduled.status == Status.PENDING
    assert found_scheduled.workout_id == test_workout.id

def test_get_one_scheduled_workout_unauthorized(client, test_scheduled_workout):
    res = client.get(f"/workouts/scheduled/{test_scheduled_workout.id}")
    
    assert res.status_code == 401

def test_get_other_user_scheduled_workout(authorized_client, test_scheduled_workout2):
    res = authorized_client.get(f"/workouts/scheduled/{test_scheduled_workout2.id}")
    
    assert res.status_code == 403

def test_get_non_existent_scheduled_workout(authorized_client):
    res = authorized_client.get(f"/workouts/scheduled/88888888")
    
    assert res.status_code == 404

def test_update_status_pending_to_active(authorized_client, test_scheduled_workout):
    res = authorized_client.patch(f"/workouts/scheduled/{test_scheduled_workout.id}/status", json={"status": "active"})
    updated = workout.ScheduledWorkoutOut(**res.json())
    
    assert res.status_code == 200
    assert updated.status == Status.ACTIVE

def test_update_status_active_to_completed(authorized_client, test_scheduled_workout_active):
    res = authorized_client.patch(f"/workouts/scheduled/{test_scheduled_workout_active.id}/status", json={"status": "completed"})
    updated = workout.ScheduledWorkoutOut(**res.json())
    
    assert res.status_code == 200
    assert updated.status == Status.COMPLETED

def test_update_status_invalid_transition(authorized_client, test_scheduled_workout):
    res = authorized_client.patch(f"/workouts/scheduled/{test_scheduled_workout.id}/status", json={"status": "completed"})
    
    assert res.status_code == 400

def test_update_status_completed_is_final(authorized_client, test_scheduled_workout_active):
    res = authorized_client.patch(f"/workouts/scheduled/{test_scheduled_workout_active.id}/status", json={"status": "completed"})
    assert res.status_code == 200
    res = authorized_client.patch(f"/workouts/scheduled/{test_scheduled_workout_active.id}/status", json={"status": "active"})
    assert res.status_code == 400

def test_delete_scheduled_workout(authorized_client, test_scheduled_workout):
    res = authorized_client.delete(f"/workouts/scheduled/{test_scheduled_workout.id}")
    
    assert res.status_code == 204

def test_delete_scheduled_workout_unauthorized(client, test_scheduled_workout):
    res = client.delete(f"/workouts/scheduled/{test_scheduled_workout.id}")
    
    assert res.status_code == 401

def test_delete_other_user_scheduled_workout(authorized_client, test_scheduled_workout2):
    res = authorized_client.delete(f"/workouts/scheduled/{test_scheduled_workout2.id}")
    
    assert res.status_code == 403

def test_create_workout_log(authorized_client, test_scheduled_workout_active, test_user):
    data = {"scheduled_workout_id": test_scheduled_workout_active.id, "duration_minutes": 75, "notes": "Felt great, PR achieved."}
    res = authorized_client.post("/workouts/logs", json=data)
    created_log = workout.WorkoutLogOut(**res.json())
    
    assert res.status_code == 201
    assert created_log.user_id == test_user["id"]
    assert created_log.scheduled_workout_id == data["scheduled_workout_id"]
    assert created_log.duration_minutes == data["duration_minutes"]
    assert created_log.notes == data["notes"]

def test_create_workout_log_auto_completes_scheduled(authorized_client, test_scheduled_workout_active):
    data = {"scheduled_workout_id": test_scheduled_workout_active.id, "duration_minutes": 75, "notes": "Felt great, PR achieved."}
    res = authorized_client.post("/workouts/logs", json=data)
    
    assert res.status_code == 201
    
    res = authorized_client.get(f"/workouts/scheduled/{test_scheduled_workout_active.id}")
    assert res.status_code == 200
    
    found_scheduled = workout.ScheduledWorkoutOut(**res.json())
    assert found_scheduled.status == Status.COMPLETED
    
def test_create_workout_log_unauthorized(client, test_scheduled_workout_active):
    res = client.post("/workouts/logs", json={"scheduled_workout_id": test_scheduled_workout_active.id, "duration_minutes": 60})
    
    assert res.status_code == 401

def test_create_workout_log_non_existent_scheduled(authorized_client):
    res = authorized_client.post("/workouts/logs", json={"scheduled_workout_id": 888888, "duration_minutes": 60})
    
    assert res.status_code == 404

def test_create_workout_log_other_user_scheduled(authorized_client, test_scheduled_workout2):
    res = authorized_client.post("/workouts/logs", json={"scheduled_workout_id": test_scheduled_workout2.id, "duration_minutes": 60})
    
    assert res.status_code == 403

def test_create_log_exercises(authorized_client, test_log, test_exercises):
    data = [
        {"exercise_id": test_exercises[0].id, "sets_completed": 3, "reps_completed": 20},
        {"exercise_id": test_exercises[5].id, "sets_completed": 3, "reps_completed": 8, "weight_used_kg": 80.0}
    ]
    res = authorized_client.post(f"/workouts/logs/{test_log.id}/exercises", json=data)
    created_log = workout.WorkoutLogOut(**res.json())
    
    assert res.status_code == 201
    assert len(created_log.log_exercises) == 2

def test_create_log_exercises_unauthorized(client, test_log, test_exercises):
    res = client.post(f"/workouts/logs/{test_log.id}/exercises", json={"exercise_id": test_exercises[0].id, "sets_completed": 3, "reps_completed": 20})
    
    assert res.status_code == 401

def test_create_log_exercises_non_existent_log(authorized_client, test_exercises):
    res = authorized_client.post("/workouts/logs/888888/exercises", json={"exercise_id": test_exercises[0].id, "sets_completed": 3, "reps_completed": 20})
    
    assert res.status_code == 404
    
def test_create_log_exercises_other_user_log(authorized_client, test_workout2, test_user2, test_exercises, session):
    scheduled = ScheduledWorkout(workout_id=test_workout2.id, user_id=test_user2['id'], scheduled_at=datetime.now(timezone.utc) + timedelta(days=1), status=Status.ACTIVE)
    session.add(scheduled)
    session.flush()
    
    log = WorkoutLog(scheduled_workout_id=scheduled.id, user_id=test_user2['id'], duration_minutes=30)
    session.add(log)
    session.commit()
    session.refresh(log)
    
    data = [{"exercise_id": test_exercises[0].id, "sets_completed": 3, "reps_completed": 10}]
    
    res = authorized_client.post(f"/workouts/logs/{log.id}/exercises", json=data)
    
    assert res.status_code == 403