from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import report
from .. import oauth2, models
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

router = APIRouter(
    prefix="/reports",
    tags=['Reports']
)

@router.get("/summary", response_model=report.WorkoutSummary)
def get_workout_summary(current_user = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    total_workouts = db.query(func.count(models.WorkoutLog.id)).filter(models.WorkoutLog.user_id == current_user.id).scalar()
    
    total_duration = db.query(func.sum(models.WorkoutLog.duration_minutes)).filter(models.WorkoutLog.user_id == current_user.id).scalar()
    
    avg_duration = db.query(func.avg(models.WorkoutLog.duration_minutes)).filter(models.WorkoutLog.user_id == current_user.id).scalar()
    
    week_start = datetime.now(timezone.utc) - timedelta(days=datetime.now(timezone.utc).weekday())
    workouts_this_week = db.query(func.count(models.WorkoutLog.id)).filter(models.WorkoutLog.user_id == current_user.id, models.WorkoutLog.completed_at >= week_start).scalar()
    
    most_trained = db.query(models.Exercise.muscle_group, func.count(models.Exercise.muscle_group).label("count")).join(models.WorkoutLogExercise, models.WorkoutLogExercise.exercise_id == models.Exercise.id).join(models.WorkoutLog, models.WorkoutLog.id == models.WorkoutLogExercise.log_id).filter(models.WorkoutLog.user_id == current_user.id).group_by(models.Exercise.muscle_group).order_by(func.count(models.Exercise.muscle_group).desc()).first()
    
    most_trained_muscle_group = most_trained.muscle_group.value if most_trained else None
    
    logs = db.query(models.WorkoutLogExercise).join(models.WorkoutLog, models.WorkoutLog.id == models.WorkoutLogExercise.log_id).filter(models.WorkoutLog.user_id == current_user.id).all()
    total_volume = sum((l.sets_completed * l.reps_completed * l.weight_used_kg) for l in logs if l.weight_used_kg is not None) or None
    
    return report.WorkoutSummary(total_workouts=total_workouts or 0, total_duration_minutes=total_duration, average_duration_minutes=float(avg_duration) if avg_duration else None, workouts_this_week=workouts_this_week or 0, most_trained_muscle_group=most_trained_muscle_group, total_volume_kg=total_volume)


@router.get("/progress/{id}", response_model=report.ExerciseProgress)
def get_exercise_progress(id: int, current_user = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    
    log_exercises = db.query(models.WorkoutLogExercise).join(models.WorkoutLog, models.WorkoutLog.id == models.WorkoutLogExercise.log_id).filter(models.WorkoutLogExercise.exercise_id == id, models.WorkoutLog.user_id == current_user.id).order_by(models.WorkoutLog.completed_at.asc()).all()
    
    data_points = []
    for le in log_exercises:
        volume = None
        if le.weight_used_kg is not None:
            volume = le.sets_completed * le.reps_completed * le.weight_used_kg
        data_points.append(report.ProgressDataPoint(completed_at=le.log.completed_at, sets_completed=le.sets_completed, reps_completed=le.reps_completed, weight_used_kg=le.weight_used_kg, volume_kg=volume))
    
    return report.ExerciseProgress(exercise_id=exercise.id, exercise_name=exercise.name, data_points=data_points)