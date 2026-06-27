import logging
from rest_framework import serializers
from .models import Task

logger = logging.getLogger(__name__)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_at']

    @staticmethod
    def validate_title(value):
        if not value or value.strip() == '':
            logger.warning('Попытка создать задачу с пустым заголовком')
            raise serializers.ValidationError("Название задачи не может быть пустым.")
        return value

    @staticmethod
    def validate_status(value):
        allowed = [choice[0] for choice in Task.STATUS_CHOICES]
        if value not in allowed:
            logger.warning('Попытка указать недопустимый статус: %s', value)
            raise serializers.ValidationError(f"Допустимые статусы: {', '.join(allowed)}")
        return value