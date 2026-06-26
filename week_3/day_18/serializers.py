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

    def validate_title(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Название задачи не может быть пустым.")
        return value

    def validate_status(self, value):
        allowed = [choice[0] for choice in Task.STATUS_CHOICES]
        if value not in allowed:
            raise serializers.ValidationError(f"Допустимые статусы: {', '.join(allowed)}")
        return value

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'created_at', 'tasks']