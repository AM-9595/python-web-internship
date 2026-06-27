import logging
from django.core.exceptions import ValidationError
from .models import Task

logger = logging.getLogger(__name__)

def change_task_status(task: Task, new_status: str) -> Task:
    logger.info('Попытка изменить статус задачи id=%s с "%s" на "%s"', task.id, task.status, new_status)

    if new_status not in dict(Task.STATUS_CHOICES):
        logger.error('Недопустимый статус: %s', new_status)
        raise ValidationError(f"Недопустимый статус: {new_status}")

    if task.status == 'done' and new_status == 'new':
        logger.warning('Попытка перевести задачу id=%s из done в new', task.id)
        raise ValidationError("Нельзя перевести задачу из статуса 'done' обратно в 'new'.")

    task.status = new_status
    task.save(update_fields=['status'])
    logger.info('Статус задачи id=%s успешно изменён на "%s"', task.id, new_status)
    return task