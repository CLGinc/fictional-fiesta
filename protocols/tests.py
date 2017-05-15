from django.test import TestCase
from django.test.client import Client
from django.core.exceptions import ValidationError

from .models import Protocol, Result, Asset
from researchers.models import Researcher, Role
from projects.models import Project


class ProtocolsTest(TestCase):
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
        self.researcher1 = Researcher.objects.get(id=1)
        self.researcher2 = Researcher.objects.get(id=2)
        self.researcher3 = Researcher.objects.get(id=3)
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
            owner=self.researcher1,
            state='created',
            protocol=self.protocol1
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected researcher cannot add results to this protocol!'],
            e.exception.messages)

    def test_create_result_when_not_owner_contributor_of_project(self):
        result = Result(
            owner=self.researcher2,
            state='created',
            protocol=self.protocol1,
            project=self.project1
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected researcher cannot add results to this project!'],
            e.exception.messages)

    def test_create_unfinished_successful_result(self):
        result = Result(
            owner=self.researcher2,
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
            owner=self.researcher3,
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
        self.assertEqual(owner, self.researcher2)

    def test_get_participants_by_role(self):
        participants_by_role = list()
        for role in self.protocol1.get_participants_by_role():
            participants_by_role.append([role[0], list(role[1])])
        expected_participants = [
            ['Owner', [Role.objects.get(protocol=self.protocol1, researcher=self.researcher2)]],
            ['Watcher', [Role.objects.get(protocol=self.protocol1, researcher=self.researcher1)]]
        ]
        self.assertEqual(participants_by_role, expected_participants)
