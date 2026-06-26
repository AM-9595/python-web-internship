from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from .services import change_task_status

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=['get'], url_path='tasks')
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        project_id = self.request.query_params.get('project_id')

        if status_param:
            queryset = queryset.filter(status=status_param)
        if project_id:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def perform_update(self, serializer):
        instance = serializer.instance
        new_status = serializer.validated_data.get('status')

        if new_status is not None and instance.status != new_status:
            try:
                change_task_status(instance, new_status)
                serializer.instance.refresh_from_db()
            except ValidationError as e:
                raise serializers.ValidationError({'status': str(e)})
        else:
            serializer.save()

    @action(detail=True, methods=['post'], url_path='comments')
    def add_comment(self, request, pk=None):
        task = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)