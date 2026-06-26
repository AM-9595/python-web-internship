from rest_framework import serializers
from .models import Project, Task, Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'project', 'title', 'description', 'status', 'created_at', 'comments']

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'tasks']