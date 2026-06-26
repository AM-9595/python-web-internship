from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer

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