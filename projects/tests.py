from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from .models import Project
from .forms import BasicProjectForm, AddElementsForm
from users.models import User, Role, Source
from protocols.models import Protocol


class ProjectModelTest(TestCase):
    fixtures = [
        'users/fixtures/users',
        'projects/fixtures/projects',
        'users/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='user1@gmail.com')
        self.user2 = User.objects.get(username='user2@gmail.com')
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.protocol6 = Protocol.objects.get(name='Protocol 6')
        self.protocol9 = Protocol.objects.get(name='Protocol 9')
        self.protocol10 = Protocol.objects.get(name='Protocol 10')

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

    def test_create_owner_role(self):
        project = Project(
            name='New Project',
        )
        project._owner = self.user1
        project.save()
        owner = project.roles.filter(role='owner')
        self.assertTrue(owner.exists())

    def test_create_roles_on_add_protocol(self):
        self.project1.protocols.add(
            self.protocol6,
            self.protocol9,
            self.protocol10
        )
        self.assertTrue(
            Role.objects.filter(
                user=self.user2,
                protocol=self.protocol6,
                role='watcher'
            ).exists()
        )
        self.assertTrue(
            Role.objects.filter(
                user=self.user1,
                protocol=self.protocol6,
                role='owner'
            ).exists()
        )
        self.assertTrue(
            Role.objects.filter(
                user=self.user2,
                protocol=self.protocol9,
                role='watcher'
            ).exists()
        )
        self.assertTrue(
            Role.objects.filter(
                user=self.user1,
                protocol=self.protocol9,
                role='contributor'
            ).exists()
        )
        self.assertTrue(
            Role.objects.filter(
                user=self.user2,
                protocol=self.protocol10,
                role='watcher'
            ).exists()
        )
        self.assertTrue(
            Role.objects.filter(
                user=self.user1,
                protocol=self.protocol10,
                role='contributor'
            ).exists()
        )

    def test_archive_project(self):
        self.project1.archive()
        self.assertTrue(self.project1.archived)


class ProjectViewTest(TestCase):
    fixtures = [
        'users/fixtures/users',
        'projects/fixtures/projects',
        'users/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(username='user1@gmail.com')
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')

    def test_get_projects_list(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('projects:projects_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_project(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('projects:project', kwargs={'project_uuid': str(self.project1.pk)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_project_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('projects:create_project')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_project_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('projects:create_project')
        response = self.client.post(
            url,
            data={'name': 'name1'}
        )
        project = self.user1.roles.get(
            role='owner',
            project__name='name1'
        ).project
        self.assertRedirects(
            response,
            reverse('projects:project', kwargs={'project_uuid': project.pk})
        )

    def test_update_project_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:update_project',
            kwargs={'project_uuid': self.project1.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_project_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:update_project',
            kwargs={'project_uuid': self.project1.pk}
        )
        redirect_url = reverse(
            'projects:project',
            kwargs={'project_uuid': self.project1.pk}
        )
        response = self.client.post(
            url,
            data={'name': 'New Project Name'}
        )
        self.project1.refresh_from_db()
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.project1.name, 'New Project Name')

    def test_archive_project_get_owner(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:archive_project',
            kwargs={'project_uuid': self.project1.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_archive_project_get_contributor(self):
        self.client.login(username='user2@gmail.com', password='user2')
        url = reverse(
            'projects:archive_project',
            kwargs={'project_uuid': self.project2.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_archive_project_get_watcher(self):
        self.client.login(username='user2@gmail.com', password='user2')
        url = reverse(
            'projects:archive_project',
            kwargs={'project_uuid': self.project1.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_archive_project_post_owner(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:archive_project',
            kwargs={'project_uuid': self.project1.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.project1.refresh_from_db()
        self.assertTrue(self.project1.archived)

    def test_archive_project_post_contributor(self):
        self.client.login(username='user2@gmail.com', password='user2')
        url = reverse(
            'projects:archive_project',
            kwargs={'project_uuid': self.project2.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.project2.refresh_from_db()
        self.assertFalse(self.project2.archived)

    def test_archive_project_post_watcher(self):
        self.client.login(username='user2@gmail.com', password='user2')
        url = reverse(
            'projects:archive_project',
            kwargs={'project_uuid': self.project1.pk}
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.project1.refresh_from_db()
        self.assertFalse(self.project1.archived)


class ProjectAjaxTest(TestCase):
    fixtures = [
        'users/fixtures/users',
        'projects/fixtures/projects',
        'users/fixtures/sources',
        'users/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.client = Client()
        self.project1 = Project.objects.get(name='Project 1')
        self.protocol8 = Protocol.objects.get(name='Protocol 8')
        self.protocol10 = Protocol.objects.get(name='Protocol 10')

    def test_get_project_protocols_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:add_protocols_to_project',
            kwargs={'project_uuid': str(self.project1.pk)}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_get_project_protocols_to_add_non_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:add_protocols_to_project',
            kwargs={'project_uuid': str(self.project1.pk)}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_project_protocols_to_add_404(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:add_protocols_to_project',
            kwargs={'project_uuid': '74369692-6844-430d-bff2-90904fc3094e'}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_post_project_protocols_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:add_protocols_to_project',
            kwargs={'project_uuid': str(self.project1.pk)}
        )
        data = {
            'element_type': 'p',
            'element_choices': [str(self.protocol10.pk), str(self.protocol8.pk)]
        }
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertRedirects(
            response,
            reverse('projects:project', kwargs={'project_uuid': str(self.project1.pk)})
        )

    def test_get_project_sources_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:project_add_sources',
            kwargs={'project_uuid': str(self.project1.pk)}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_get_project_sources_to_add_non_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:project_add_sources',
            kwargs={'project_uuid': str(self.project1.pk)}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_project_sources_to_add_404(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:project_add_sources',
            kwargs={'project_uuid': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'}
        )
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)

    def test_post_project_sources_to_add(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'projects:project_add_sources',
            kwargs={'project_uuid': str(self.project1.pk)}
        )
        data = {
            'element_type': 's',
            'element_choices': ['1', '2']
        }
        response = self.client.post(
            url,
            data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertRedirects(
            response,
            reverse('projects:project', kwargs={'project_uuid': str(self.project1.pk)})
        )


class ProjectFormTest(TestCase):
    fixtures = [
        'users/fixtures/users',
        'users/fixtures/sources',
        'projects/fixtures/projects',
        'users/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='user1@gmail.com')
        self.user2 = User.objects.get(username='user2@gmail.com')
        self.project1 = Project.objects.get(name='Project 1')
        self.protocol1 = Protocol.objects.get(name='Protocol 1')
        self.protocol2 = Protocol.objects.get(name='Protocol 2')
        self.protocol3 = Protocol.objects.get(name='Protocol 3')
        self.protocol4 = Protocol.objects.get(name='Protocol 4')
        self.protocol5 = Protocol.objects.get(name='Protocol 5')
        self.protocol6 = Protocol.objects.get(name='Protocol 6')
        self.protocol7 = Protocol.objects.get(name='Protocol 7')
        self.protocol8 = Protocol.objects.get(name='Protocol 8')
        self.protocol9 = Protocol.objects.get(name='Protocol 9')
        self.protocol10 = Protocol.objects.get(name='Protocol 10')
        self.source1 = Source.objects.get(name='Source 1')
        self.source2 = Source.objects.get(name='Source 2')
        self.source3 = Source.objects.get(name='Source 3')

    def test_new_project_form_empty(self):
        form = BasicProjectForm(data={})
        self.assertFalse(form.is_valid())

    def test_new_project_form_mandatory_fields(self):
        data = {
            'name': 'Project 1'
        }
        form = BasicProjectForm(data, user=self.user1)
        self.assertTrue(form.is_valid())
        project = form.save()
        self.assertIsInstance(project, Project)
        self.assertTrue(
            self.user1.roles.filter(
                project=project, role='owner'
            )
        )

    def test_new_project_form_all_fields(self):
        data = {
            'name': 'Project 1',
            'description': 'Project 1 Description'
        }
        form = BasicProjectForm(data, user=self.user1)
        self.assertTrue(form.is_valid())
        project = form.save()
        self.assertIsInstance(project, Project)
        self.assertTrue(
            self.user1.roles.filter(
                project=project, role='owner'
            )
        )

    def test_add_elements_form_empty(self):
        form = AddElementsForm(
            data={},
            user=self.user1,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())

    def test_add_elements_form_protocols_all_fields(self):
        data = {
            'element_type': 'p',
            'element_choices': [str(self.protocol6.pk), str(self.protocol8.pk)]
        }
        form = AddElementsForm(
            data,
            user=self.user1,
            selected_project=self.project1
        )
        self.assertTrue(form.is_valid())

    def test_add_elements_form_protocols_queryset(self):
        data = {
            'element_type': 'p',
            'element_choices': [str(self.protocol6.pk), str(self.protocol8.pk)]
        }
        form = AddElementsForm(
            data,
            user=self.user1,
            selected_project=self.project1
        )
        protocols_to_add = [
            self.protocol10,
            self.protocol8,
            self.protocol6
        ]
        self.assertEqual(
            list(form.fields['element_choices'].queryset),
            protocols_to_add
        )

    def test_add_elements_form_protocols_before_validation(self):
        data = {
            'element_type': 'p',
            'element_choices': [str(self.protocol6.pk), str(self.protocol8.pk)]
        }
        form = AddElementsForm(
            data,
            user=self.user1,
            selected_project=self.project1
        )
        with self.assertRaises(AttributeError):
            form.add_elements(self.project1)

    def test_add_elements_form_protocols_add_elements(self):
        data = {
            'element_type': 'p',
            'element_choices': [str(self.protocol6.pk), str(self.protocol8.pk)]
        }
        form = AddElementsForm(
            data,
            user=self.user1,
            selected_project=self.project1
        )
        self.assertTrue(form.is_valid())
        form.add_elements(self.project1)
        expected_protocols = [
            self.protocol8,
            self.protocol7,
            self.protocol6,
            self.protocol3,
            self.protocol1
        ]
        self.assertEqual(
            list(self.project1.protocols.all()),
            expected_protocols
        )

    def test_add_elements_form_protocols_watcher(self):
        data = {
            'element_type': 'p',
            'element_choices': [str(self.protocol6.pk), str(self.protocol8.pk)]
        }
        form = AddElementsForm(
            data,
            user=self.user2,
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
            user=self.user1,
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
            user=self.user1,
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
            user=self.user1,
            selected_project=self.project1
        )
        sources_to_add = [
            self.source3,
            self.source2,
            self.source1
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
            user=self.user1,
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
            user=self.user1,
            selected_project=self.project1
        )
        form.is_valid()
        form.add_elements(self.project1)
        expected_sourcess = [
            self.source1,
            self.source2,
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
            user=self.user2,
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
            user=self.user1,
            selected_project=self.project1
        )
        self.assertFalse(form.is_valid())
        self.assertTrue(form.fields['element_choices'].queryset)
        self.assertIn('element_choices', form.errors.keys())
