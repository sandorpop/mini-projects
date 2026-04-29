from fastapi import status, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import models, oauth2

def get_exercise_or_404(id: int, db: Session = Depends(get_db)) -> models.Exercise:
    exercise = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise

def get_own_exercise(
    exercise = Depends(get_exercise_or_404), 
    current_user = Depends(oauth2.get_current_user)
    ) -> models.Exercise:
    
    if exercise.is_seeded:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot modify seeded exercises")
    
    if exercise.created_by != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform this action")
    return exercise