import re

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .utils import generate_uid
from .models import Project
from .forms import NewProjectForm, AddElementsForm
from researchers.models import Researcher


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

    def test_get_projects_list(self):
        self.client.login(username='user0@gmail.com', password='user0')
        url = reverse('projects_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        self.client.login(username='user0@gmail.com', password='user0')
        url = reverse('project', kwargs={'project_uid': '0f570c02'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_generate_unique_id(self):
        key = generate_uid()
        self.assertEqual(len(key), 8)
        self.assertTrue(re.match(r'([A-Za-z]|[0-9]){8}', key))


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
        self.researcher0 = Researcher.objects.get(
            user__username='user0@gmail.com'
        )
        self.researcher1 = Researcher.objects.get(
            user__username='user1@gmail.com'
        )
        self.project1 = Project.objects.get(id=1)

    def test_new_project_form_empty(self):
        form = NewProjectForm()
        self.assertFalse(form.is_valid())

    def test_new_project_form_mandatory_fields(self):
        data = {
            'name': 'Project 1'
        }
        form = NewProjectForm(data)
        self.assertTrue(form.is_valid())
        project = form.save(self.researcher0)
        self.assertIsInstance(project, Project)
        self.assertTrue(
            self.researcher0.roles.filter(
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
        project = form.save(self.researcher0)
        self.assertIsInstance(project, Project)
        self.assertTrue(
            self.researcher0.roles.filter(
                project=project, role='owner'
            )
        )

    def test_add_elements_form_empty(self):
        form = AddElementsForm(
            researcher=self.researcher0,
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
            researcher=self.researcher0,
            selected_project=self.project1
        )
        self.assertTrue(form.is_valid())

    def test_add_elements_form_sources_all_fields(self):
        data = {
            'element_type': 's',
            'element_choices': ['1', '2']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher0,
            selected_project=self.project1
        )
        self.assertTrue(form.is_valid())

    def test_add_elements_form_protocols_watcher(self):
        data = {
            'element_type': 'p',
            'element_choices': ['fba17387', '8f4a328c']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
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
        self.assertFalse(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())

    def test_add_elements_form_sources_watcher(self):
        data = {
            'element_type': 's',
            'element_choices': ['4', '5']
        }
        form = AddElementsForm(
            data,
            researcher=self.researcher1,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())
        self.assertFalse(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())

