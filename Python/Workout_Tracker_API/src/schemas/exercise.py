from pydantic import BaseModel
from ..models import Category, MuscleGroup
from datetime import datetime
from typing import Optional

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str]=None
    category: Category
    muscle_group: MuscleGroup
    
class ExerciseCreate(ExerciseBase):
    pass

class ExerciseUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[Category] = None
    muscle_group: Optional[MuscleGroup] = None

class ExerciseOut(ExerciseBase):
    id: int
    is_seeded: bool
    created_by: Optional[int]=None
    created_at: datetime
    model_config = {"from_attributes": True}
    
class ExerciseFilter(BaseModel):
    category: Optional[Category]=None
    muscle_group: Optional[MuscleGroup]=None