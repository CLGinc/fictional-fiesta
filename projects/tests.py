import re

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .utils import generate_uid
from .models import Project
from .forms import NewProjectForm, AddElementsForm
from researchers.models import Researcher, Role, Source
from protocols.models import Protocol


class ProjectsTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'projects/fixtures/projects',
        'researchers/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.client = Client()
        self.project1 = Project.objects.get(id=1)
        self.project2 = Project.objects.get(id=2)

    def test_get_projects_list(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('projects_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('project', kwargs={'project_uid': '0f570c02'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_generate_unique_id(self):
        key = generate_uid()
        self.assertEqual(len(key), 8)
        self.assertTrue(re.match(r'([A-Za-z]|[0-9]){8}', key))

    def test_get_participants_by_role_all(self):
        participants = self.project2.get_participants_by_role()
        participants = [[a[0], list(a[1])] for a in participants]
        expected_participants = [
            ['Owner', [Role.objects.get(id=13)]],
            ['Contributor', [Role.objects.get(id=5)]],
            ['Watcher', [Role.objects.get(id=18)]],
        ]
        self.assertEqual(participants, expected_participants)

    def test_get_participants_by_role(self):
        participants = self.project1.get_participants_by_role()
        participants = [[a[0], list(a[1])] for a in participants]
        expected_participants = [
            ['Owner', [Role.objects.get(id=6)]],
            ['Watcher', [Role.objects.get(id=15)]],
        ]
        self.assertEqual(participants, expected_participants)


class ProjectsAjaxTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'projects/fixtures/projects',
        'researchers/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.client = Client()

    def test_get_project_protocols_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_protocols_to_add',
            kwargs={'project_uid': '0f570c02'}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_get_project_protocols_to_add_non_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_protocols_to_add',
            kwargs={'project_uid': '0f570c02'}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_project_protocols_to_add_404(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_protocols_to_add',
            kwargs={'project_uid': 'test1234'}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_post_project_protocols_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_protocols_to_add',
            kwargs={'project_uid': '0f570c02'}
        )
        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)

    def test_get_project_sources_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_sources_to_add',
            kwargs={'project_uid': '0f570c02'}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_get_project_sources_to_add_non_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_sources_to_add',
            kwargs={'project_uid': '0f570c02'}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_project_sources_to_add_404(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_sources_to_add',
            kwargs={'project_uid': 'test1234'}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_post_project_sources_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'project_get_sources_to_add',
            kwargs={'project_uid': '0f570c02'}
        )
        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 403)


class ProjectsFormsTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'projects/fixtures/projects',
        'researchers/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.researcher1 = Researcher.objects.get(id=1)
        self.researcher2 = Researcher.objects.get(id=2)
        self.project1 = Project.objects.get(id=1)

    def test_new_project_form_empty(self):
        form = NewProjectForm(data={})
        self.assertFalse(form.is_valid())

    def test_new_project_form_mandatory_fields(self):
        data = {
            'name': 'Project 1'
        }
        form = NewProjectForm(data)
        self.assertTrue(form.is_valid())
        project = form.save(self.researcher1)
        self.assertIsInstance(project, Project)
        self.assertTrue(
            self.researcher1.roles.filter(
                project=project, role='owner'
            )
        )

    def test_new_project_form_all_fields(self):
        data = {
            'name': 'Project 1',
            'description': 'Project 1 Description'
        }
        form = NewProjectForm(data)
        self.assertTrue(form.is_valid())
        project = form.save(self.researcher1)
        self.assertIsInstance(project, Project)
        self.assertTrue(
            self.researcher1.roles.filter(
                project=project, role='owner'
            )
        )

    def test_add_elements_form_empty(self):
        form = AddElementsForm(
            data={},
            researcher=self.researcher1,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())

    def test_add_elements_form_protocols_all_fields(self):
        data = {
            'element_type': 'p',
            'element_choices': ['fba17387', '8f4a328c']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        self.assertTrue(form.is_valid())

    def test_add_elements_form_protocols_queryset(self):
        data = {
            'element_type': 'p',
            'element_choices': ['fba17387', '8f4a328c']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        protocols_to_add = [
            Protocol.objects.get(unique_id='fba17387'),
            Protocol.objects.get(unique_id='8f4a328c'),
            Protocol.objects.get(unique_id='52944cc7')
        ]
        self.assertEqual(
            list(form.fields['element_choices'].queryset),
            protocols_to_add
        )

    def test_add_elements_form_protocols_before_validation(self):
        data = {
            'element_type': 'p',
            'element_choices': ['fba17387', '8f4a328c']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        with self.assertRaises(AttributeError):
            form.add_elements(self.project1)

    def test_add_elements_form_protocols_add_elements(self):
        data = {
            'element_type': 'p',
            'element_choices': ['fba17387', '8f4a328c']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        form.is_valid()
        form.add_elements(self.project1)
        expected_protocols = [
            Protocol.objects.get(unique_id='635be0c0'),
            Protocol.objects.get(unique_id='3e39fed1'),
            Protocol.objects.get(unique_id='fba17387'),
            Protocol.objects.get(unique_id='55980c82'),
            Protocol.objects.get(unique_id='8f4a328c')
        ]
        self.assertEqual(
            list(self.project1.protocols.all()),
            expected_protocols
        )

    def test_add_elements_form_protocols_watcher(self):
        data = {
            'element_type': 'p',
            'element_choices': ['fba17387', '8f4a328c']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher2,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())
        self.assertFalse(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())

    def test_add_elements_form_protocols_not_in_queryset(self):
        data = {
            'element_type': 'p',
            'element_choices': ['test0', 'test1']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())

    def test_add_elements_form_sources_all_fields(self):
        data = {
            'element_type': 's',
            'element_choices': ['1', '2']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        self.assertTrue(form.is_valid())

    def test_add_elements_form_sources_queryset(self):
        data = {
            'element_type': 's',
            'element_choices': ['1', '2']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        sources_to_add = [
            Source.objects.get(id=3),
            Source.objects.get(id=2),
            Source.objects.get(id=1)
        ]
        self.assertEqual(
            list(form.fields['element_choices'].queryset),
            sources_to_add
        )

    def test_add_elements_form_sources_before_validation(self):
        data = {
            'element_type': 's',
            'element_choices': ['1', '2']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        with self.assertRaises(AttributeError):
            form.add_elements(self.project1)

    def test_add_elements_form_sources_add_elements(self):
        data = {
            'element_type': 's',
            'element_choices': ['1', '2']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        form.is_valid()
        form.add_elements(self.project1)
        expected_sourcess = [
            Source.objects.get(id=1),
            Source.objects.get(id=2),
        ]
        self.assertEqual(
            list(self.project1.sources.all()),
            expected_sourcess
        )

    def test_add_elements_form_sources_watcher(self):
        data = {
            'element_type': 's',
            'element_choices': ['4', '5']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher2,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())
        self.assertFalse(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())

    def test_add_elements_form_sources_not_in_queryset(self):
        data = {
            'element_type': 's',
            'element_choices': ['0', '1']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())
