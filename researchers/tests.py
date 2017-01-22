from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError


from .models import Researcher, Role, Source
from projects.models import Project
from protocols.models import Protocol


class ResearchersTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols']

    def setUp(self):
        self.client = Client()
        self.project1 = Project.objects.get(id=1)
        self.project2 = Project.objects.get(id=2)
        self.project3 = Project.objects.get(id=3)
        self.researcher0 = Researcher.objects.get(
            user__username='user0@gmail.com'
        )
        self.researcher1 = Researcher.objects.get(
            user__username='user1@gmail.com'
        )
        self.researcher2 = Researcher.objects.get(
            user__username='user2@gmail.com'
        )
        self.tempuser = Researcher.objects.get(
            user__username='tempuser@gmail.com'
        )
        self.protocol1 = Protocol.objects.get(id=1)
        self.roles_per_projects = {
            self.researcher0: {
                'owner': [self.project1, self.project2],
                'contributor': [self.project3],
                },
            self.researcher1: {
                'contributor': [self.project2, self.project3],
                'watcher': [self.project1],
                },
            self.researcher2: {
                'watcher': [self.project1, self.project2],
                'owner': [self.project3],
                },
        }

    def test_get_roles_owners(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher0.get_roles(scope='project', roles=['owner']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(
            self.researcher0).get('owner')
        self.assertEqual(
            len(roles_list_researcher0),
            len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher1.get_roles(scope='project', roles=['owner']))
        self.assertEqual(projects_list_researcher1, [])

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher2.get_roles(scope='project', roles=['owner']))
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
                scope='project',
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
                scope='project',
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
                scope='project',
                roles=['contributor']))
        self.assertEqual(projects_list_researcher2, [])

    def test_get_roles_watchers(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher0.get_roles(scope='project', roles=['watcher']))
        self.assertEqual(roles_list_researcher0, [])

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher1.get_roles(scope='project', roles=['watcher']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(
            self.researcher1).get('watcher')
        self.assertEqual(
            len(projects_list_researcher1),
            len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher2.get_roles(scope='project', roles=['watcher']))
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
            project=self.project1,
            protocol=self.protocol1,
            role='watcher'
        )
        with self.assertRaises(ValidationError) as e:
            role.clean()
        self.assertEqual(
            ["You cannot select project and protocol for the same role!"],
            e.exception.messages)

    def test_role_without_project_and_protocol(self):
        role = Role(
            researcher=self.tempuser,
            role='watcher'
        )
        with self.assertRaises(ValidationError) as e:
            role.clean()
        self.assertEqual(
            ["You must choose either project or protocol!"],
            e.exception.messages)

    def test_add_second_owner_to_project(self):
        role = Role(
            researcher=self.tempuser,
            project=self.project1,
            role='owner'
        )
        with self.assertRaises(ValidationError) as e:
            role.clean()
        self.assertEqual(
            ["There is already an owner of this project!"],
            e.exception.messages)

    def test_add_second_owner_to_protocol(self):
        role = Role(
            researcher=self.tempuser,
            protocol=self.protocol1,
            role='owner'
        )
        with self.assertRaises(ValidationError) as e:
            role.clean()
        self.assertEqual(
            ["There is already an owner of this protocol!"],
            e.exception.messages)

    def test_get_protocols_to_add(self):
        protocols = list(self.researcher0.get_protocols_to_add(self.project1))
        expected_protocols = [
            Protocol.objects.get(unique_id='fba17387'),
            Protocol.objects.get(unique_id='8f4a328c'),
            Protocol.objects.get(unique_id='52944cc7')
        ]
        self.assertEqual(protocols, expected_protocols)

    def test_get_sources_to_add(self):
        sources = list(self.researcher0.get_sources_to_add(self.project1))
        expected_sources = [
            Source.objects.get(id=3),
            Source.objects.get(id=2),
            Source.objects.get(id=1)
        ]
        self.assertEqual(sources, expected_sources)

    def test_can_edit(self):
        self.assertTrue(self.researcher0.can_edit(self.project1))
        self.assertFalse(self.researcher1.can_edit(self.project1))

    def test_get_projects_to_edit(self):
        projects = list(self.researcher1.get_projects_to_edit())
        expected_projects = [
            Project.objects.get(id=2),
            Project.objects.get(id=3)
        ]
        self.assertEqual(projects, expected_projects)

    def test_get_protocols_to_edit(self):
        protocols = list(self.researcher1.get_protocols_to_edit())
        expected_protocols = [
            Protocol.objects.get(id=1)
        ]
        self.assertEqual(protocols, expected_protocols)

    def test_get_login(self):
        url = reverse('login_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_login(self):
        url = reverse('login_user')
        data = {
            'email': 'user0@gmail.com',
            'password': 'user0'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/projects/list/')

    def test_post_login_redirect_to_project(self):
        url = reverse('login_user') + '?next=/projects/0f570c02/'
        data = {
            'email': 'user0@gmail.com',
            'password': 'user0'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/projects/0f570c02/')

    def test_get_logout(self):
        self.client.login(username='user0@gmail.com', password='user0')
        url = reverse('logout_user')
        response = self.client.get(url)
        self.assertRedirects(response, '/login/')

    def test_get_register(self):
        url = reverse('register_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_register(self):
        url = reverse('register_user')
        data = {
            'email': 'userreg@gmail.com',
            'password1': 'hr192$^8rh198',
            'password2': 'hr192$^8rh198',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/projects/list/')
