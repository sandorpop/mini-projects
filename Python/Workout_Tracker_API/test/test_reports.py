from src.schemas import report

def test_get_summary_no_data(authorized_client):
    res = authorized_client.get("/reports/summary")
    summary = report.WorkoutSummary(**res.json())
    
    assert res.status_code == 200
    assert summary.total_workouts == 0
    assert summary.workouts_this_week == 0
    assert summary.total_duration_minutes == None
    assert summary.average_duration_minutes == None
    assert summary.most_trained_muscle_group == None
    assert summary.total_volume_kg == None

def test_get_summary_with_data(authorized_client, test_log, test_log_exercises):
    res = authorized_client.get("/reports/summary")
    summary = report.WorkoutSummary(**res.json())
    
    assert res.status_code == 200
    assert summary.total_workouts == 1
    assert summary.workouts_this_week == 1
    assert summary.total_duration_minutes == 45
    assert summary.average_duration_minutes == 45.0
    assert summary.most_trained_muscle_group == "chest"
    assert summary.total_volume_kg == 2560.0 # 4 * 8 * 80.0 = 2560.0

def test_get_summary_unauthorized(client):
    res = client.get("/reports/summary")
    
    assert res.status_code == 401

def test_get_exercise_progress(authorized_client, test_log, test_log_exercises, test_exercises):
    res = authorized_client.get(f"/reports/progress/{test_exercises[5].id}")
    progress = report.ExerciseProgress(**res.json())
    
    assert res.status_code == 200
    assert progress.exercise_id == test_exercises[5].id
    assert progress.exercise_name == "Bench Press"
    assert len(progress.data_points) == 1
    assert progress.data_points[0].sets_completed == 4
    assert progress.data_points[0].reps_completed == 8
    assert progress.data_points[0].weight_used_kg == 80.0
    assert progress.data_points[0].volume_kg == 4 * 8 * 80.0

def test_get_exercise_progress_no_logs(authorized_client, test_exercises):
    res = authorized_client.get(f"/reports/progress/{test_exercises[0].id}")
    progress = report.ExerciseProgress(**res.json())
    
    assert res.status_code == 200
    assert len(progress.data_points) == 0

def test_get_exercise_progress_non_existent(authorized_client):
    res = authorized_client.get("/reports/progress/88888")
    
    assert res.status_code == 404

def test_get_exercise_progress_unauthorized(client, test_exercises):
    res = client.get(f"/reports/progress/{test_exercises[5].id}")
    
    assert res.status_code == 401