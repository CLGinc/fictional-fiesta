from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


class ProjectsTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'projects/fixtures/projects',
        'researchers/fixtures/roles']

    def setUp(self):
        self.client = Client()

    def test_get_projects_list(self):
        self.client.login(username='user0', password='user0')
        url = reverse('projects_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        self.client.login(username='user0', password='user0')
        url = reverse('project', kwargs={'project_id': '0f570c02'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
