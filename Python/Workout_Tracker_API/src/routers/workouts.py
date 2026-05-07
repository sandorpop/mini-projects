from fastapi import status, Depends, APIRouter, Response, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, dependencies, oauth2
from ..schemas import workout
from typing import List, Optional
from datetime import datetime

router = APIRouter(
    prefix="/workouts",
    tags=['Workouts']
)

VALID_TRANSITIONS = {
    models.Status.PENDING: [models.Status.ACTIVE, models.Status.CANCELLED],
    models.Status.ACTIVE: [models.Status.COMPLETED, models.Status.CANCELLED],
    models.Status.COMPLETED: [],
    models.Status.CANCELLED: []
}

@router.post("/", response_model=workout.WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(workout_data: workout.WorkoutCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    try:
        new_workout = models.Workout(owner_id=current_user.id, title=workout_data.title, description=workout_data.description)
        db.add(new_workout)
        db.flush()
        for exercise in workout_data.exercises:
            new_exercise = models.WorkoutExercise(workout_id=new_workout.id, **exercise.model_dump())
            db.add(new_exercise)
        db.commit()
        db.refresh(new_workout)
        return new_workout
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create workout")
    
@router.get("/", response_model=List[workout.WorkoutOut])
def get_workouts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), title: Optional[str]=None):
    query = db.query(models.Workout).filter(models.Workout.owner_id == current_user.id)
    if title:
        query = query.filter(models.Workout.title.contains(title))
    return query.all()

@router.get("/scheduled", response_model=List[workout.ScheduledWorkoutOut])
def get_scheduled_workouts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), status_filter: Optional[models.Status] = None, from_date: Optional[datetime] = None, to_date: Optional[datetime] = None):
    query = db.query(models.ScheduledWorkout).filter(models.ScheduledWorkout.user_id == current_user.id)
    if status_filter is not None:
        query = query.filter(models.ScheduledWorkout.status == status_filter)
    if from_date is not None:
        query = query.filter(models.ScheduledWorkout.scheduled_at >= from_date)
    if to_date is not None:
        query = query.filter(models.ScheduledWorkout.scheduled_at <= to_date)
    
    return query.order_by(models.ScheduledWorkout.scheduled_at.asc()).all()

@router.get("/scheduled/{id}", response_model=workout.ScheduledWorkoutOut)
def get_one_scheduled_workout(workout = Depends(dependencies.get_own_scheduled_workout)):
    return workout

@router.get("/{id}", response_model=workout.WorkoutOut)
def get_one_workout(workout = Depends(dependencies.get_own_workout)):
    return workout

@router.put("/{id}", response_model=workout.WorkoutOut)
def update_workout(workout_data: workout.WorkoutUpdate, current_workout = Depends(dependencies.get_own_workout), db: Session = Depends(get_db)):
    update_data = workout_data.model_dump(exclude_unset=True)
    exercises = update_data.pop("exercises", None)

    db.query(models.Workout).filter(models.Workout.id == current_workout.id).update(update_data, synchronize_session=False)

    if exercises is not None:
        db.query(models.WorkoutExercise).filter(models.WorkoutExercise.workout_id == current_workout.id).delete(synchronize_session=False)
        for exercise in exercises:
            new_exercise = models.WorkoutExercise(workout_id=current_workout.id, **exercise)
            db.add(new_exercise)

    db.commit()
    updated_workout = db.query(models.Workout).filter(models.Workout.id == current_workout.id).first()
    return updated_workout

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(current_workout = Depends(dependencies.get_own_workout), db: Session = Depends(get_db)):
    db.delete(current_workout)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{id}/schedule", response_model=workout.ScheduledWorkoutOut, status_code=status.HTTP_201_CREATED)
def create_scheduled_workout(workout_data: workout.ScheduledWorkoutCreate, current_user = Depends(oauth2.get_current_user), current_workout = Depends(dependencies.get_own_workout), db: Session = Depends(get_db)):
    new_workout = models.ScheduledWorkout(workout_id=current_workout.id, user_id=current_user.id, scheduled_at=workout_data.scheduled_at)
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

@router.patch("/scheduled/{id}/status", response_model=workout.ScheduledWorkoutOut, status_code=status.HTTP_200_OK)
def set_scheduled_workout_status(new_status: workout.ScheduledWorkoutStatusUpdate, current_workout = Depends(dependencies.get_own_scheduled_workout), db: Session = Depends(get_db)):
    if new_status.status not in VALID_TRANSITIONS[current_workout.status]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot transition from {current_workout.status} to {new_status.status}.")
    setattr(current_workout, "status", new_status.status)
    db.commit()
    db.refresh(current_workout)
    return current_workout

@router.delete("/scheduled/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scheduled_workout(current_workout = Depends(dependencies.get_own_scheduled_workout), db: Session = Depends(get_db)):
    db.delete(current_workout)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)