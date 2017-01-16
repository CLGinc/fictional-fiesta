import re

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .utils import generate_uid
from .models import Project


class ProjectsTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'projects/fixtures/projects',
        'researchers/fixtures/roles',
        'protocols/fixtures/protocols']

    def setUp(self):
        self.client = Client()

    def test_get_projects_list(self):
        self.client.login(username='user0', password='user0')
        url = reverse('projects_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        self.client.login(username='user0', password='user0')
        url = reverse('project', kwargs={'project_uid': '0f570c02'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_generate_unique_id(self):
        key = generate_uid()
        self.assertEqual(len(key), 8)
        self.assertTrue(re.match(r'([A-Za-z]|[0-9]){8}', key))

    def test_generated_unique_id_is_unique(self):
        for i in range(1000000):
            Project.objects.create(
                name='Project {}'.format(i)
            )
