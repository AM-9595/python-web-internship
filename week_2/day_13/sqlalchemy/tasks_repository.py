from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdateStatus

def create_task(db: Session, task: TaskCreate, user_id: int) -> Task:
    db_task = Task(title=task.title, status=task.status, user_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, user_id: int) -> list[Task]:
    return db.query(Task).filter(Task.user_id == user_id).all()

def get_task(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_status(db: Session, task_id: int, new_status: str) -> Task | None:
    task = get_task(db, task_id)
    if not task:
        return None
    task.status = new_status
    db.commit()
    db.refresh(task)
    return task