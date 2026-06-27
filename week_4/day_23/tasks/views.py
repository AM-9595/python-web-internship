import logging
from django.http import Http404
from rest_framework.exceptions import NotFound
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rest_framework import serializers as drf_serializers
from .models import Task
from .serializers import TaskSerializer
from .services import change_task_status

logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            logger.error('Задача не найдена (id=%s)', self.kwargs.get('pk'))
            raise NotFound('Задача не найдена')

    def perform_create(self, serializer):
        task = serializer.save()
        logger.info('Создана задача: id=%s, title=%s', task.id, task.title)

    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = serializer.validated_data.get('status')
        if new_status is not None and instance.status != new_status:
            try:
                change_task_status(instance, new_status)
                instance.refresh_from_db()
                logger.info('Задача id=%s обновлена (статус)', instance.id)
            except ValidationError as e:
                logger.error('Ошибка валидации при изменении статуса задачи id=%s: %s', instance.id, str(e))
                raise drf_serializers.ValidationError({'status': str(e)})
        else:
            serializer.save()
            logger.info('Задача id=%s обновлена (поля кроме статуса)', instance.id)

    @action(detail=True, methods=['post'], url_path='comments')
    def add_comment(self, request, pk=None):
        task = self.get_object()

        logger.info('Запрос на добавление комментария к задаче id=%s', task.id)
        return Response({'detail': 'Метод не реализован'}, status=status.HTTP_501_NOT_IMPLEMENTED)