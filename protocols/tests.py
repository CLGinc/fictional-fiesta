from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from .models import Protocol, Result, Asset
from users.models import User, Role
from projects.models import Project


class ProtocolModelTest(TestCase):
    fixtures = [
        'users/fixtures/users',
        'projects/fixtures/projects',
        'users/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='user1@gmail.com')
        self.user2 = User.objects.get(username='user2@gmail.com')
        self.user3 = User.objects.get(username='user3@gmail.com')
        self.protocol1 = Protocol.objects.get(name='Protocol 1')
        self.protocol2 = Protocol.objects.get(name='Protocol 2')
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.asset1 = Asset.objects.get(id=1)
        self.asset2 = Asset.objects.get(id=2)
        self.asset3 = Asset.objects.get(id=3)
        self.asset4 = Asset.objects.get(id=4)
        self.asset5 = Asset.objects.get(id=5)
        self.asset6 = Asset.objects.get(id=6)

    def test_create_result_when_not_owner_contributor_of_protocol(self):
        result = Result(
            owner=self.user1,
            state='created',
            protocol=self.protocol1
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected user cannot add results to this protocol!'],
            e.exception.messages)

    def test_create_result_when_not_owner_contributor_of_project(self):
        result = Result(
            owner=self.user2,
            state='created',
            protocol=self.protocol1,
            project=self.project1
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected user cannot add results to this project!'],
            e.exception.messages)

    def test_create_unfinished_successful_result(self):
        result = Result(
            owner=self.user2,
            state='created',
            is_successful=True,
            protocol=self.protocol1
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['Unfinished result cannot be marked successful!'],
            e.exception.messages)

    def test_create_result_where_protocol_does_not_belong_to_project(self):
        result = Result(
            owner=self.user3,
            state='created',
            protocol=self.protocol2,
            project=self.project1
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected protocol does not belong to the selected project!'],
            e.exception.messages)

    def test_get_assets_by_category(self):
        assets = self.protocol1.get_assets_by_category()
        materials = [a for a in assets[0][1]]
        expected_materials = [self.asset1, self.asset2, self.asset3, self.asset5]
        self.assertEqual(materials, expected_materials)
        equipment = [a for a in assets[1][1]]
        expected_equipment = [self.asset4, self.asset6]
        self.assertEqual(equipment, expected_equipment)

    def test_get_owner(self):
        owner = self.protocol1.get_owner()
        self.assertEqual(owner, self.user2)

    def test_get_participants_by_role(self):
        participants_by_role = list()
        for role in self.protocol1.get_participants_by_role():
            participants_by_role.append([role[0], list(role[1])])
        expected_participants = [
            ['Owner', [Role.objects.get(protocol=self.protocol1, user=self.user2)]],
            ['Watcher', [Role.objects.get(protocol=self.protocol1, user=self.user1)]]
        ]
        self.assertEqual(participants_by_role, expected_participants)

    def test_create_owner_role(self):
        protocol = Protocol(
            name='New Protocol',
            label='modified',
            procedure='{"steps":[{"description":"Step 1 description","title":"Step 1"},{"description":"Step 2 description","title":"Step 2"},{"description":"Step 3 description","title":"Step 3"},{"description":"Step 4 description","title":"Step 4"},{"description":"Step 5 description","title":"Step 5"},{"description":"Step 6 description","title":"Step 6"},{"description":"Step 7 description","title":"Step 7"}]}',
            last_modified_by=self.user1
        )
        protocol._owner = self.user1
        protocol.save()
        owner = protocol.roles.filter(role='owner')
        self.assertTrue(owner.exists())


class ProtocolViewTest(TestCase):
    fixtures = [
        'users/fixtures/users',
        'projects/fixtures/projects',
        'users/fixtures/roles',
        'protocols/fixtures/protocols'
    ]

    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.get(username='user1@gmail.com')
        self.protocol1 = Protocol.objects.get(name='Protocol 1')
        self.protocol3 = Protocol.objects.get(name='Protocol 3')
        self.protocol3_result = Result.objects.get(pk='833eaf8d-4154-45b9-b96a-2d9ee27f704a')

    def test_get_protocols_list(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('protocols_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_protocol(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('protocol', kwargs={'protocol_uuid': str(self.protocol1.pk)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_protocol_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_protocol')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_protocol_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_protocol')
        response = self.client.post(
            url,
            data={
                'name': 'New Protocol',
                'label': 'modified',
                'procedure': '{"steps":[{"description":"Step 1 description","title":"Step 1"},{"description":"Step 2 description","title":"Step 2"},{"description":"Step 3 description","title":"Step 3"},{"description":"Step 4 description","title":"Step 4"},{"description":"Step 5 description","title":"Step 5"},{"description":"Step 6 description","title":"Step 6"},{"description":"Step 7 description","title":"Step 7"}]}',
            }
        )
        protocol = self.user1.roles.get(
            role='owner',
            protocol__name='New Protocol'
        ).protocol
        self.assertRedirects(
            response,
            reverse('protocol', kwargs={'protocol_uuid': protocol.pk})
        )

    def test_update_protocol_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'update_protocol',
            kwargs={'protocol_uuid': self.protocol6.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_protocol_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'update_protocol',
            kwargs={'protocol_uuid': self.protocol6.pk}
        )
        redirect_url = reverse(
            'protocol',
            kwargs={'protocol_uuid': self.protocol3.pk}
        )
        response = self.client.post(
            url,
            data={
                'name': 'New Protocol Name',
                'label': 'modified',
                'procedure': '{"steps":[{"description":"Step 1 description","title":"Step 1"},{"description":"Step 2 description","title":"Step 2"},{"description":"Step 3 description","title":"Step 3"},{"description":"Step 4 description","title":"Step 4"},{"description":"Step 5 description","title":"Step 5"},{"description":"Step 6 description","title":"Step 6"},{"description":"Step 7 description","title":"Step 7"}]}',
            }
        )
        self.protocol3.refresh_from_db()
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.protocol3.name, 'New Protocol Name')

    def test_create_protocol_result_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'create_protocol_result',
            kwargs={'protocol_uuid': self.protocol3.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_protocol_result_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'create_protocol_result',
            kwargs={'protocol_uuid': str(self.protocol3.pk)}
        )
        response = self.client.post(
            url,
            data={
                'title': 'Result title',
                'protocol': str(self.protocol3.pk),
                'note': 'New Note',
                'state': 'created',
                'independent_variable': 'Salt Concentration (%)',
                'dependent_variable': 'Light Transmittance (%T)',
                'data_columns': '{"dependent_variable":[{"data":[5,4,3,2,1],"title":"Trial 1"},{"data":[5,4,3,2,1],"title":"Trial 2"}],"independent_variable":[{"data":[0,2,4,6,8],"title":"Independent Variable"}]}',
                'data_type_dependent': 'number',
                'data_type_independent': 'number'
            }
        )
        result = self.protocol3.results.all().order_by('-datetime_created')[0]
        self.assertRedirects(
            response,
            reverse(
                'protocol_result',
                kwargs={
                    'protocol_uuid': self.protocol3.pk,
                    'result_uuid': result.pk
                }
            )
        )

    def test_update_protocol_result_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'update_protocol_result',
            kwargs={
                'protocol_uuid': self.protocol3.pk,
                'result_uuid': str(self.protocol3_result.pk)
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_protocol_result_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'update_protocol_result',
            kwargs={
                'protocol_uuid': self.protocol3.pk,
                'result_uuid': str(self.protocol3_result.pk)
            }
        )
        redirect_url = reverse(
            'protocol_result',
            kwargs={
                'protocol_uuid': self.protocol3.pk,
                'result_uuid': str(self.protocol3_result.pk)
            }
        )
        response = self.client.post(
            url,
            data={
                'title': 'Result title',
                'protocol': str(self.protocol3.pk),
                'note': 'New Note',
                'state': 'created',
                'independent_variable': 'Salt Concentration (%)',
                'dependent_variable': 'Light Transmittance (%T)',
                'data_columns': '{"dependent_variable":[{"data":[5,4,3,2,1],"title":"Trial 1"},{"data":[5,4,3,2,1],"title":"Trial 2"}],"independent_variable":[{"data":[0,2,4,6,8],"title":"Independent Variable"}]}',
                'data_type_dependent': 'number',
                'data_type_independent': 'number'
            }
        )
        self.protocol3_result.refresh_from_db()
        self.assertRedirects(response, redirect_url)
        self.assertEqual(self.protocol3_result.note, 'New Note')
        self.assertEqual(self.protocol3_result.title, 'Result title')

    def test_protocol_result_get(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'protocol_result',
            kwargs={
                'protocol_uuid': self.protocol3.pk,
                'result_uuid': str(self.protocol3_result.pk)
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_protocol_result_get_404(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'protocol_result',
            kwargs={
                'protocol_uuid': self.protocol3.pk,
                'result_uuid': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_protocol_result_post(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse(
            'protocol_result',
            kwargs={
                'protocol_uuid': self.protocol3.pk,
                'result_uuid': str(self.protocol3_result.pk)
            }
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 405)
