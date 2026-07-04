import logging
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Team, Project, Task, Comment

logger = logging.getLogger(__name__)
User = get_user_model()

def create_team(name, owner):
    team = Team.objects.create(name=name, owner=owner)
    team.members.add(owner)
    logger.info("Team created: id=%s, name=%s, owner_id=%s", team.id, team.name, owner.id)
    return team

def add_member_to_team(team_id, user_id):
    team = get_object_or_404(Team, id=team_id)
    user = get_object_or_404(User, id=user_id)
    team.members.add(user)
    logger.info("User %s added to team %s", user.id, team.id)
    return team

def create_project(name, description, team_id, created_by):
    team = get_object_or_404(Team, id=team_id)
    if created_by not in team.members.all():
        logger.warning("User %s not in team %s, cannot create project", created_by.id, team.id)
        raise PermissionError("User is not a member of this team")
    project = Project.objects.create(name=name, description=description, team=team, created_by=created_by)
    logger.info("Project created: id=%s, name=%s, team_id=%s", project.id, project.name, team.id)
    return project

def create_task(title, description, project_id, assigned_to_id, created_by):
    project = get_object_or_404(Project, id=project_id)
    if created_by not in project.team.members.all():
        logger.warning("User %s not in team %s, cannot create task", created_by.id, project.team.id)
        raise PermissionError("User is not a member of the team")
    assigned_to = None
    if assigned_to_id:
        assigned_to = get_object_or_404(User, id=assigned_to_id)
        if assigned_to not in project.team.members.all():
            logger.warning("Assigned user %s not in team %s", assigned_to.id, project.team.id)
            raise PermissionError("Assigned user is not a member of the team")
    task = Task.objects.create(
        title=title,
        description=description,
        project=project,
        assigned_to=assigned_to,
        created_by=created_by
    )
    logger.info("Task created: id=%s, title=%s, project_id=%s", task.id, task.title, project.id)
    return task

def create_comment(task_id, user, text):
    task = get_object_or_404(Task, id=task_id)
    if user not in task.project.team.members.all():
        logger.warning("User %s not in team %s, cannot comment", user.id, task.project.team.id)
        raise PermissionError("User is not a member of the team")
    comment = Comment.objects.create(task=task, user=user, text=text)
    logger.info("Comment created: id=%s, task_id=%s, user_id=%s", comment.id, task.id, user.id)
    return comment