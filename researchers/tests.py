from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse


from .models import Researcher
from projects.models import Project


class ProjectsTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'projects/fixtures/projects',
        'projects/fixtures/roles']

    def setUp(self):
        self.client = Client()
        self.project0 = Project.objects.get(name='Project 0')
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.researcher0 = Researcher.objects.get(user__username='user0')
        self.researcher1 = Researcher.objects.get(user__username='user1')
        self.researcher2 = Researcher.objects.get(user__username='user2')
        self.roles_per_projects = {
            self.researcher0: {
                'owner': [self.project0, self.project1],
                'contributor': [self.project2],
                },
            self.researcher1: {
                'contributor': [self.project1, self.project2],
                'watcher': [self.project0],
                },
            self.researcher2: {
                'watcher': [self.project0, self.project1],
                'owner': [self.project2],
                },
        }

    def test_get_projects_by_roles_owners(self):
        # Check data for Researcher 0
        projects_list_researcher0 = list(self.researcher0.get_projects_by_roles(['owner']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(self.researcher0).get('owner')
        self.assertEqual(len(projects_list_researcher0), len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(self.researcher1.get_projects_by_roles(['owner']))
        self.assertEqual(projects_list_researcher1, [])

        # Check data for Researcher 2
        projects_list_researcher2 = list(self.researcher2.get_projects_by_roles(['owner']))
        expected_projects_list_researcher2 = self.roles_per_projects.get(self.researcher2).get('owner')
        self.assertEqual(len(projects_list_researcher2), len(expected_projects_list_researcher2))
        for project in expected_projects_list_researcher2:
            self.assertIn(project, expected_projects_list_researcher2)

    def test_get_projects_by_roles_contributors(self):
        # Check data for Researcher 0
        projects_list_researcher0 = list(self.researcher0.get_projects_by_roles(['contributor']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(self.researcher0).get('contributor')
        self.assertEqual(len(projects_list_researcher0), len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(self.researcher1.get_projects_by_roles(['contributor']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(self.researcher1).get('contributor')
        self.assertEqual(len(projects_list_researcher1), len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(self.researcher2.get_projects_by_roles(['contributor']))
        self.assertEqual(projects_list_researcher2, [])

    def test_get_projects_by_roles_watchers(self):
        # Check data for Researcher 0
        projects_list_researcher0 = list(self.researcher0.get_projects_by_roles(['watcher']))
        self.assertEqual(projects_list_researcher0, [])

        # Check data for Researcher 1
        projects_list_researcher1 = list(self.researcher1.get_projects_by_roles(['watcher']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(self.researcher1).get('watcher')
        self.assertEqual(len(projects_list_researcher1), len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(self.researcher2.get_projects_by_roles(['watcher']))
        expected_projects_list_researcher2 = self.roles_per_projects.get(self.researcher2).get('watcher')
        self.assertEqual(len(projects_list_researcher2), len(expected_projects_list_researcher2))
        for project in expected_projects_list_researcher2:
            self.assertIn(project, expected_projects_list_researcher2)
