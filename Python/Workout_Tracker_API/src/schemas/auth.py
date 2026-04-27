from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    model_config = {"from_attributes": True}
    
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]=None