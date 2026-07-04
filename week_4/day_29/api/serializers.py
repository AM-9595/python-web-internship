from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Team, Project, Task, Comment

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class TeamSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'owner', 'members')

class ProjectSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'team', 'created_by', 'created_at')
        read_only_fields = ('created_at',)

class TaskSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'project', 'status', 'assigned_to',
                  'created_by', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def validate_status(self, value):
        if self.instance and self.instance.status == 'done' and value != 'done':
            raise serializers.ValidationError("Cannot change status from 'done' to another.")
        return value

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'task', 'user', 'text', 'created_at')
        read_only_fields = ('created_at',)