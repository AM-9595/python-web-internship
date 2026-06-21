from sqlalchemy.orm import Session
from tasks_repository import create_task, get_tasks_by_user, update_task_status
from schemas import TaskCreate

def create_task_service(db: Session, task_data: TaskCreate, user_id: int):
    return create_task(db, task_data, user_id)

def get_user_tasks_service(db: Session, user_id: int):
    return get_tasks_by_user(db, user_id)

def update_task_status_service(db: Session, task_id: int, new_status: str):
    return update_task_status(db, task_id, new_status)