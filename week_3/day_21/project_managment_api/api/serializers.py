from rest_framework import serializers
from .models import Project, Task, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tasks_count = serializers.IntegerField(source='tasks.count', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'owner', 'tasks_count']

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'project', 'assigned_to',
                  'created_at', 'updated_at', 'project_name', 'assigned_to_username']

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'task', 'author', 'author_username', 'created_at']