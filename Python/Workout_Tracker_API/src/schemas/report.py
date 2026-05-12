from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class WorkoutSummary(BaseModel):
    total_workouts: int
    total_duration_minutes: Optional[int] = None
    average_duration_minutes: Optional[float] = None
    workouts_this_week: int
    most_trained_muscle_group: Optional[str] = None
    total_volume_kg: Optional[float] = None
    model_config = {"from_attributes": True}

class ProgressDataPoint(BaseModel):
    completed_at: datetime
    sets_completed: int
    reps_completed: int
    weight_used_kg: Optional[float] = None
    volume_kg: Optional[float] = None
    model_config = {"from_attributes": True}
    
class ExerciseProgress(BaseModel):
    exercise_id: int
    exercise_name: str
    data_points: List[ProgressDataPoint]
    model_config = {"from_attributes": True}