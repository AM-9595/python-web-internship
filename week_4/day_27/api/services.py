from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Team, Project, Task, Comment

User = get_user_model()

def create_team(name, owner):
    team = Team.objects.create(name=name, owner=owner)
    team.members.add(owner)
    return team

def add_member_to_team(team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    user = get_object_or_404(User, id=user_id)
    team.members.add(user)
    return team

def create_project(name, description, team_id, created_by):
    team = get_object_or_404(Team, id=team_id)
    if created_by not in team.members.all():
        raise PermissionError("User is not a member of this team")
    return Project.objects.create(name=name, description=description, team=team, created_by=created_by)

def create_task(title, description, project_id, assigned_to_id, created_by):
    project = get_object_or_404(Project, id=project_id)
    if created_by not in project.team.members.all():
        raise PermissionError("User is not a member of the team")
    assigned_to = None
    if assigned_to_id:
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        if assigned_to not in project.team.members.all():
            raise PermissionError("Assigned user is not a member of the team")
    return Task.objects.create(
        title=title,
        description=description,
        project=project,
        assigned_to=assigned_to,
        created_by=created_by
    )

def create_comment(task_id, user, text):
    task = get_object_or_404(Task, id=task_id)
    if user not in task.project.team.members.all():
        raise PermissionError("User is not a member of the team")
    return Comment.objects.create(task=task, user=user, text=text)