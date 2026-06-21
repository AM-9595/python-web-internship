from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

class TaskCreate(BaseModel):
    title: str
    status: Optional[str] = "new"

class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    user_id: int

class TaskUpdateStatus(BaseModel):
    status: str  # new, in_progress, done