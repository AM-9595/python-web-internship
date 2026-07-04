from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Team, Project, Task, Comment
from .serializers import (
    TeamSerializer, ProjectSerializer, TaskSerializer, CommentSerializer,
    UserRegistrationSerializer
)
from .permissions import IsTeamMember, IsProjectMember, IsTaskAccessible, IsCommentAccessible
from .services import create_team, create_project, create_task, create_comment

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = []

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Team.objects.filter(Q(members=self.request.user) | Q(owner=self.request.user))

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTeamMember()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        team = create_team(request.data.get('name'), request.user)
        serializer = self.get_serializer(team)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        team = self.get_object()
        if team.owner != request.user:
            return Response({'detail': 'Only owner can add members.'},
                            status=status.HTTP_403_FORBIDDEN)
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'detail': 'user_id required.'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, id=user_id)
        if user in team.members.all():
            return Response({'detail': 'User already in team.'},
                            status=status.HTTP_400_BAD_REQUEST)
        team.members.add(user)
        return Response({'detail': f'User {user.username} added to team.'},
                        status=status.HTTP_200_OK)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(team__members=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsProjectMember()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            project = create_project(
                name=request.data.get('name'),
                description=request.data.get('description', ''),
                team_id=request.data.get('team'),
                created_by=request.user
            )
            serializer = self.get_serializer(project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(project__team__members=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsTaskAccessible()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            task = create_task(
                title=request.data.get('title'),
                description=request.data.get('description', ''),
                project_id=request.data.get('project'),
                assigned_to_id=request.data.get('assigned_to'),
                created_by=request.user
            )
            serializer = self.get_serializer(task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(task__project__team__members=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsCommentAccessible()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        try:
            comment = create_comment(
                task_id=request.data.get('task'),
                user=request.user,
                text=request.data.get('text')
            )
            serializer = self.get_serializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except PermissionError as e:
            return Response({'detail': str(e)}, status=status.HTTP_403_FORBIDDEN)