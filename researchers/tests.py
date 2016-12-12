from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError


from .models import Researcher, Role
from projects.models import Project
from protocols.models import Protocol


class ProjectsTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols']

    def setUp(self):
        self.client = Client()
        self.project0 = Project.objects.get(name='Project 0')
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.researcher0 = Researcher.objects.get(user__username='user0')
        self.researcher1 = Researcher.objects.get(user__username='user1')
        self.researcher2 = Researcher.objects.get(user__username='user2')
        self.tempuser = Researcher.objects.get(user__username='tempuser')
        self.protocol0 = Protocol.objects.get(name='Protocol 0')
        self.protocol0 = Protocol.objects.get(name='Protocol 1')
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

    def test_get_roles_owners(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher0.get_roles(scope='projects', roles=['owner']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(
            self.researcher0).get('owner')
        self.assertEqual(
            len(roles_list_researcher0),
            len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher1.get_roles(scope='projects', roles=['owner']))
        self.assertEqual(projects_list_researcher1, [])

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher2.get_roles(scope='projects', roles=['owner']))
        expected_projects_list_researcher2 = self.roles_per_projects.get(
            self.researcher2).get('owner')
        self.assertEqual(
            len(projects_list_researcher2),
            len(expected_projects_list_researcher2))
        for project in expected_projects_list_researcher2:
            self.assertIn(project, expected_projects_list_researcher2)

    def test_get_roles_contributors(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher0.get_roles(
                scope='projects',
                roles=['contributor']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(
            self.researcher0).get('contributor')
        self.assertEqual(
            len(roles_list_researcher0),
            len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher1.get_roles(
                scope='projects',
                roles=['contributor']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(
            self.researcher1).get('contributor')
        self.assertEqual(
            len(projects_list_researcher1),
            len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher2.get_roles(
                scope='projects',
                roles=['contributor']))
        self.assertEqual(projects_list_researcher2, [])

    def test_get_roles_watchers(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher0.get_roles(scope='projects', roles=['watcher']))
        self.assertEqual(roles_list_researcher0, [])

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher1.get_roles(scope='projects', roles=['watcher']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(
            self.researcher1).get('watcher')
        self.assertEqual(
            len(projects_list_researcher1),
            len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher2.get_roles(scope='projects', roles=['watcher']))
        expected_projects_list_researcher2 = self.roles_per_projects.get(
            self.researcher2).get('watcher')
        self.assertEqual(
            len(projects_list_researcher2),
            len(expected_projects_list_researcher2))
        for project in expected_projects_list_researcher2:
            self.assertIn(project, expected_projects_list_researcher2)

    def test_add_role_with_project_and_protocol(self):
        role = Role(
            researcher=self.tempuser,
            project=self.project0,
            protocol=self.protocol0,
            role='watcher'
        )
        self.assertRaises(ValidationError, role.save())

    def test_role_without_project_and_protocol(self):
        role = Role(
            researcher=self.tempuser,
            role='watcher'
        )
        self.assertRaises(ValidationError, role.save())

    def test_add_second_owner_to_project(self):
        role = Role(
            researcher=self.tempuser,
            project=self.project0,
            role='owner'
        )
        self.assertRaises(ValidationError, role.save())

    def test_add_second_owner_to_protocol(self):
        role = Role(
            researcher=self.tempuser,
            protocol=self.protocol0,
            role='owner'
        )
        self.assertRaises(ValidationError, role.save())
