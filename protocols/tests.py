from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from .models import Protocol, Result
from researchers.models import Researcher
from projects.models import Project


class ProtocolTest(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'projects/fixtures/projects',
        'researchers/fixtures/roles',
        'protocols/fixtures/protocols']

    def setUp(self):
        self.client = Client()
        self.researcher0 = Researcher.objects.get(user__username='user0')
        self.researcher1 = Researcher.objects.get(user__username='user1')
        self.protocol0 = Protocol.objects.get(name='Protocol 0')
        self.project0 = Project.objects.get(name='Project 0')
        self.project1 = Project.objects.get(name='Project 1')

    def test_create_result_when_not_owner_contributor_of_protocol(self):
        result = Result(
            owner=self.researcher0,
            state='created',
            protocol=self.protocol0
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected researcher cannot add results to this protocol!'],
            e.exception.messages)

    def test_create_result_when_not_owner_contributor_of_project(self):
        result = Result(
            owner=self.researcher1,
            state='created',
            protocol=self.protocol0,
            project=self.project0
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected researcher cannot add results to this project!'],
            e.exception.messages)

    def test_create_unfinished_successful_result(self):
        result = Result(
            owner=self.researcher1,
            state='created',
            is_successful=True,
            protocol=self.protocol0
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['Unfinished result cannot be marked successful!'],
            e.exception.messages)

    def test_create_result_where_protocol_does_not_belong_to_project(self):
        result = Result(
            owner=self.researcher1,
            state='created',
            protocol=self.protocol0,
            project=self.project0
        )
        with self.assertRaises(ValidationError) as e:
            result.clean()
        self.assertEqual(
            ['The selected researcher cannot add results to this project!'],
            e.exception.messages)
