from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import TaskCreate, TaskResponse, TaskUpdateStatus
from tasks_service import create_task_service, get_user_tasks_service, update_task_status_service
from users_service import get_user_service

router = APIRouter(prefix="/users/{user_id}/tasks", tags=["tasks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[TaskResponse])
def get_tasks(user_id: int, db: Session = Depends(get_db)):
    user = get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_user_tasks_service(db, user_id)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(user_id: int, task_data: TaskCreate, db: Session = Depends(get_db)):
    user = get_user_service(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_task_service(db, task_data, user_id)

task_router = APIRouter(prefix="/tasks", tags=["tasks"])

@task_router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(task_id: int, status_data: TaskUpdateStatus, db: Session = Depends(get_db)):
    task = update_task_status_service(db, task_id, status_data.status)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task