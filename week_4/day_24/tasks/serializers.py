from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project, Task, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']

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
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'created_at', 'tasks']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()