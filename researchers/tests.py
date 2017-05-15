from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError


from .models import Researcher, Role, Source
from projects.models import Project
from protocols.models import Protocol

from .forms import RoleListForm


class ResearcherModelTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.project3 = Project.objects.get(name='Project 3')
        self.researcher1 = Researcher.objects.get(id=1)
        self.researcher2 = Researcher.objects.get(id=2)
        self.researcher3 = Researcher.objects.get(id=3)
        self.tempuser = Researcher.objects.get(id=1001)
        self.protocol1 = Protocol.objects.get(name='Protocol 1')
        self.protocol6 = Protocol.objects.get(name='Protocol 6')
        self.protocol8 = Protocol.objects.get(name='Protocol 8')
        self.protocol10 = Protocol.objects.get(name='Protocol 10')
        self.roles_per_projects = {
            self.researcher1: {
                'owner': [self.project1, self.project2],
                'contributor': [self.project3],
            },
            self.researcher2: {
                'contributor': [self.project2, self.project3],
                'watcher': [self.project1],
            },
            self.researcher3: {
                'watcher': [self.project2],
                'owner': [self.project3],
            },
        }

    def test_get_roles_owners(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher1.get_roles(scope='project', roles=['owner']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(
            self.researcher1).get('owner')
        self.assertEqual(
            len(roles_list_researcher0),
            len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher2.get_roles(scope='project', roles=['owner']))
        self.assertEqual(projects_list_researcher1, [])

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher3.get_roles(scope='project', roles=['owner']))
        expected_projects_list_researcher2 = self.roles_per_projects.get(
            self.researcher3).get('owner')
        self.assertEqual(
            len(projects_list_researcher2),
            len(expected_projects_list_researcher2))
        for project in expected_projects_list_researcher2:
            self.assertIn(project, expected_projects_list_researcher2)

    def test_get_roles_contributors(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher1.get_roles(
                scope='project',
                roles=['contributor']))
        expected_projects_list_researcher0 = self.roles_per_projects.get(
            self.researcher1).get('contributor')
        self.assertEqual(
            len(roles_list_researcher0),
            len(expected_projects_list_researcher0))
        for project in expected_projects_list_researcher0:
            self.assertIn(project, expected_projects_list_researcher0)

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher2.get_roles(
                scope='project',
                roles=['contributor']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(
            self.researcher2).get('contributor')
        self.assertEqual(
            len(projects_list_researcher1),
            len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher3.get_roles(
                scope='project',
                roles=['contributor']))
        self.assertEqual(projects_list_researcher2, [])

    def test_get_roles_watchers(self):
        # Check data for Researcher 0
        roles_list_researcher0 = list(
            self.researcher1.get_roles(scope='project', roles=['watcher']))
        self.assertEqual(roles_list_researcher0, [])

        # Check data for Researcher 1
        projects_list_researcher1 = list(
            self.researcher2.get_roles(scope='project', roles=['watcher']))
        expected_projects_list_researcher1 = self.roles_per_projects.get(
            self.researcher2).get('watcher')
        self.assertEqual(
            len(projects_list_researcher1),
            len(expected_projects_list_researcher1))
        for project in expected_projects_list_researcher1:
            self.assertIn(project, expected_projects_list_researcher1)

        # Check data for Researcher 2
        projects_list_researcher2 = list(
            self.researcher3.get_roles(scope='project', roles=['watcher']))
        expected_projects_list_researcher2 = self.roles_per_projects.get(
            self.researcher3).get('watcher')
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
        protocols = list(self.researcher1.get_protocols_to_add(self.project1))
        expected_protocols = [
            self.protocol10,
            self.protocol8,
            self.protocol6
        ]
        self.assertEqual(protocols, expected_protocols)

    def test_get_sources_to_add(self):
        sources = list(self.researcher1.get_sources_to_add(self.project1))
        expected_sources = [
            Source.objects.get(id=3),
            Source.objects.get(id=2),
            Source.objects.get(id=1)
        ]
        self.assertEqual(sources, expected_sources)

    def test_can_edit(self):
        self.assertTrue(self.researcher1.can_edit(self.project1))
        self.assertFalse(self.researcher2.can_edit(self.project1))

    def test_get_projects_to_edit(self):
        projects = list(self.researcher2.get_projects_to_edit())
        expected_projects = [
            self.project3,
            self.project2
        ]
        self.assertEqual(projects, expected_projects)

    def test_get_protocols_to_edit(self):
        protocols = list(self.researcher2.get_protocols_to_edit())
        expected_protocols = [
            self.protocol1
        ]
        self.assertEqual(protocols, expected_protocols)


class ResearcherViewTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.client = Client()

    def test_get_login(self):
        url = reverse('login_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_login(self):
        url = reverse('login_user')
        data = {
            'email': 'user1@gmail.com',
            'password': 'user1'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/project/list/')

    def test_post_login_redirect_to_project(self):
        url = reverse('login_user') + '?next=/project/808d85c6-8fdb-478d-994a-aab8496ef4cb/'
        data = {
            'email': 'user1@gmail.com',
            'password': 'user1'
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, '/project/808d85c6-8fdb-478d-994a-aab8496ef4cb/')

    def test_get_logout(self):
        self.client.login(username='user1@gmail.com', password='user1')
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
        self.assertRedirects(response, '/project/list/')


class ResearcherFormTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols']

    def setUp(self):
        self.researcher1 = Researcher.objects.get(id=1)
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.project3 = Project.objects.get(name='Project 3')

    def test_project_roles_list_form_empty(self):
        form = RoleListForm(
            data={},
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())

    def test_project_roles_list_form_all_fields(self):
        data = {
            'name': 'Project 1',
            'created_from': '2016-01-01',
            'created_to': '2016-02-01',
            'role': ['owner'],
            'order_by': 'name',
            'order_type': 'asc'
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())

    def test_project_roles_list_form_name(self):
        data = {
            'name': 'Project 1',
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project1, researcher=self.researcher1)
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)

    def test_project_roles_list_form_created_from(self):
        data = {
            'created_from': '2016-11-23',
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project3, researcher=self.researcher1)
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)

    def test_project_roles_list_form_created_to(self):
        data = {
            'created_to': '2016-11-22',
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project2, researcher=self.researcher1),
            Role.objects.get(project=self.project1, researcher=self.researcher1),
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)

    def test_project_roles_list_form_role(self):
        data = {
            'role': ['owner', 'watcher'],
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project2, researcher=self.researcher1),
            Role.objects.get(project=self.project1, researcher=self.researcher1),
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)

    def test_project_roles_list_form_default_order(self):
        form = RoleListForm(
            data={},
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project3, researcher=self.researcher1),
            Role.objects.get(project=self.project2, researcher=self.researcher1),
            Role.objects.get(project=self.project1, researcher=self.researcher1),
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)

    def test_project_roles_list_form__order_by_name_default_order_type(self):
        data = {
            'order_by': 'name',
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project1, researcher=self.researcher1),
            Role.objects.get(project=self.project2, researcher=self.researcher1),
            Role.objects.get(project=self.project3, researcher=self.researcher1),
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)

    def test_project_roles_list_form__order_by_role_descending(self):
        data = {
            'order_by': 'role',
            'order_type': 'desc'
        }
        form = RoleListForm(
            data=data,
            researcher=self.researcher1,
            scope='project'
        )
        self.assertTrue(form.is_valid())
        expected_projects = [
            Role.objects.get(project=self.project1, researcher=self.researcher1),
            Role.objects.get(project=self.project2, researcher=self.researcher1),
            Role.objects.get(project=self.project3, researcher=self.researcher1),
        ]
        projects = list(form.roles)
        self.assertEqual(expected_projects, projects)
