from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .exercise import ExerciseOut
from ..models import Status

class WorkoutExerciseBase(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    weight_kg: Optional[float] = None
    order: int
    
class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass

class WorkoutExerciseOut(WorkoutExerciseBase):
    id: int
    created_at: datetime
    exercise: ExerciseOut
    model_config = {"from_attributes": True}


class WorkoutBase(BaseModel):
    title: str
    description: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    exercises: List[WorkoutExerciseCreate]
    
class WorkoutUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    exercises: Optional[List[WorkoutExerciseCreate]] = None
    
class WorkoutOut(WorkoutBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    exercises: List[WorkoutExerciseOut]
    model_config = {"from_attributes": True}
    
    
class ScheduledWorkoutBase(BaseModel):
    workout_id: int
    scheduled_at: datetime
    
class ScheduledWorkoutCreate(BaseModel):
    scheduled_at: datetime

class ScheduledWorkoutUpdate(BaseModel):
    workout_id: Optional[int] = None
    scheduled_at: Optional[datetime] = None

class ScheduledWorkoutOut(ScheduledWorkoutBase):
    id: int
    user_id: int
    status: Status
    created_at: datetime
    updated_at: datetime
    workout: WorkoutOut
    model_config = {"from_attributes": True}
    
class ScheduledWorkoutStatusUpdate(BaseModel):
    status: Status