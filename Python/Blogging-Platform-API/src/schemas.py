from pydantic import BaseModel
from typing import List
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime