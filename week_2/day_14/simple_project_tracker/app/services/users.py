from sqlalchemy.orm import Session
from app.repositories.users import create_user, get_user, get_users, delete_user
from app.schemas import UserCreate

def create_user_service(db: Session, user_data: UserCreate):
    # проверка на существование email можно добавить здесь
    return create_user(db, user_data)

def get_user_service(db: Session, user_id: int):
    return get_user(db, user_id)

def get_users_service(db: Session):
    return get_users(db)

def delete_user_service(db: Session, user_id: int):
    return delete_user(db, user_id)