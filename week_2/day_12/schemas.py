# schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr   # автоматическая валидация email
    age: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None