from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Team, Project, Task, Comment

User = get_user_model()

class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
        self.team = Team.objects.create(name='Team A', owner=self.user1)
        self.team.members.add(self.user1)
        self.project = Project.objects.create(name='Project 1', description='desc', team=self.team, created_by=self.user1)
        self.task = Task.objects.create(
            title='Task 1',
            description='desc',
            project=self.project,
            status='new',
            created_by=self.user1
        )
        self.client = APIClient()

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_register_user(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'pass123', 'email': 'new@example.com'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_get_token(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'user1', 'password': 'pass123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_create_team_authenticated(self):
        self.authenticate(self.user1)
        url = reverse('team-list')
        data = {'name': 'New Team'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_add_member_owner_only(self):
        self.authenticate(self.user1)
        url = reverse('team-add-member', args=[self.team.id])
        data = {'user_id': self.user2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user2, self.team.members.all())

    def test_add_member_non_owner_forbidden(self):
        self.authenticate(self.user2)
        url = reverse('team-add-member', args=[self.team.id])
        data = {'user_id': self.user1.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_project_team_member(self):
        self.authenticate(self.user1)
        url = reverse('project-list')
        data = {'name': 'New Project', 'team': self.team.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_create_task_team_member(self):
        self.authenticate(self.user1)
        url = reverse('task-list')
        data = {'title': 'New Task', 'project': self.project.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_change_status_from_done_to_new_forbidden(self):
        self.task.status = 'done'
        self.task.save()
        self.authenticate(self.user1)
        url = reverse('task-detail', args=[self.task.id])
        data = {'status': 'new'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Cannot change status', response.data['status'][0])

    def test_cannot_see_other_team_projects(self):
        other_team = Team.objects.create(name='Other', owner=self.user2)
        other_project = Project.objects.create(name='Other Proj', team=other_team, created_by=self.user2)
        self.authenticate(self.user1)
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.project.id)

    def test_create_comment_on_own_task(self):
        self.authenticate(self.user1)
        url = reverse('comment-list')
        data = {'task': self.task.id, 'text': 'Nice task'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment_on_foreign_task_forbidden(self):
        other_team = Team.objects.create(name='Other', owner=self.user2)
        other_project = Project.objects.create(name='Other Proj', team=other_team, created_by=self.user2)
        other_task = Task.objects.create(title='Other Task', project=other_project, created_by=self.user2)
        self.authenticate(self.user1)
        url = reverse('comment-list')
        data = {'task': other_task.id, 'text': 'Should fail'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_task_filter_by_status(self):
        self.authenticate(self.user1)
        url = reverse('task-list') + '?status=new'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        url = reverse('task-list') + '?status=done'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 0)