from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    category: str
    tags: List[str]
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}

class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    owner: UserOut
    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email: EmailStr
    password: str
        
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]=None