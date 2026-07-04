from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Team

class IsTeamMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Team):
            if request.method in SAFE_METHODS:
                return request.user in obj.members.all() or request.user == obj.owner
            return request.user == obj.owner
        return False

class IsProjectMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.team.members.all()

class IsTaskAccessible(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.project.team.members.all()

class IsCommentAccessible(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.task.project.team.members.all()