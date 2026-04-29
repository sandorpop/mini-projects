from fastapi import status, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, dependencies, oauth2
from ..schemas import exercise
from typing import List, Optional

router = APIRouter(
    prefix="/exercises",
    tags=['Exercises']
)

@router.get("/", response_model=List[exercise.ExerciseOut])
def get_exercises(db: Session = Depends(get_db), category: Optional[models.Category]=None, muscle_group: Optional[models.MuscleGroup]=None):
    query = db.query(models.Exercise)
    if category:
        query = query.filter(models.Exercise.category == category)
    
    if muscle_group:
        query = query.filter(models.Exercise.muscle_group == muscle_group)
        
    return query.all()

@router.get("/{id}", response_model=exercise.ExerciseOut)
def get_one_exercise(exercise = Depends(dependencies.get_exercise_or_404)):
    return exercise

@router.post("/", response_model=exercise.ExerciseOut, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise_data: exercise.ExerciseCreate, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    new_exercise = models.Exercise(created_by=current_user.id, is_seeded=False, **exercise_data.model_dump())
    
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    
    return new_exercise

@router.put("/{id}", response_model=exercise.ExerciseOut)
def update_exercise(exercise_data: exercise.ExerciseUpdate, current_exercise = Depends(dependencies.get_own_exercise), db: Session = Depends(get_db)):
    for key, value in exercise_data.model_dump(exclude_unset=True).items():
        setattr(current_exercise, key, value)
    
    db.commit()
    db.refresh(current_exercise)
    return current_exercise

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise(current_exercise = Depends(dependencies.get_own_exercise), db: Session = Depends(get_db)):
    db.delete(current_exercise)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)