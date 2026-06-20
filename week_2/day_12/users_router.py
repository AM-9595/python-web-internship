# users_router.py
from fastapi import APIRouter, HTTPException, status
from schemas import UserCreate, UserResponse
from users_service import (
    create_user as service_create_user,
    get_user as service_get_user,
    get_all_users as service_get_all,
    delete_user as service_delete_user
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_users():
    users = service_get_all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = service_get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):
    try:
        new_user = service_create_user(
            name=user_data.name,
            email=user_data.email,
            age=user_data.age
        )
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Если ошибка связана с дубликатом email или другой БД-ошибкой
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    deleted = service_delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return  # 204 No Content