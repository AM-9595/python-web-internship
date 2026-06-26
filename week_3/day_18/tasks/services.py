from django.core.exceptions import ValidationError
from .models import Task

def change_task_status(task: Task, new_status: str) -> Task:
    if new_status not in dict(Task.STATUS_CHOICES):
        raise ValidationError(f"Недопустимый статус: {new_status}")

    if task.status == 'done' and new_status == 'new':
        raise ValidationError("Нельзя перевести задачу из статуса 'done' обратно в 'new'.")

    task.status = new_status
    task.save(update_fields=['status'])
    return task