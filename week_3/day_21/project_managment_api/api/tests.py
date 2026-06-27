from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Project, Task, Comment

class ProjectAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', owner=self.user)

    def test_create_project(self):
        data = {'name': 'New Project', 'description': 'Desc'}
        response = self.client.post('/api/projects/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    def test_list_projects(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_project(self):
        response = self.client.get(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Project')

    def test_update_project(self):
        data = {'name': 'Updated Project', 'description': 'Updated desc'}
        response = self.client.put(f'/api/projects/{self.project.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')

    def test_delete_project(self):
        response = self.client.delete(f'/api/projects/{self.project.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 0)

class TaskAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', owner=self.user)
        self.task = Task.objects.create(title='Test Task', project=self.project, status='new')

    def test_create_task(self):
        data = {'title': 'New Task', 'project': self.project.id, 'status': 'new'}
        response = self.client.post('/api/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_filter_tasks_by_status(self):
        response = self.client.get('/api/tasks/?status=new')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_filter_tasks_by_project(self):
        response = self.client.get(f'/api/tasks/?project={self.project.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class CommentAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', owner=self.user)
        self.task = Task.objects.create(title='Test Task', project=self.project, status='new')
        self.comment = Comment.objects.create(text='Test comment', task=self.task, author=self.user)

    def test_create_comment(self):
        data = {'text': 'New comment', 'task': self.task.id, 'author': self.user.id}
        response = self.client.post('/api/comments/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_list_comments(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)