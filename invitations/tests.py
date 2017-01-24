from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.test.client import Client
from django.core.urlresolvers import reverse

from .models import Invitation
from .forms import CreateInvitationForm, AcceptInvitationForm
from researchers.models import Researcher, Role
from projects.models import Project
from protocols.models import Protocol


class InvitationsTests(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols',
    ]

    def setUp(self):
        self.client = Client()
        self.researcher1 = Researcher.objects.get(id=1)
        self.researcher2 = Researcher.objects.get(id=2)
        self.researcher3 = Researcher.objects.get(id=3)
        self.project1 = Project.objects.get(id=1)
        self.protocol1 = Protocol.objects.get(id=1)

    def test_invitation_without_project_or_protocol(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher1,
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["You must choose either project or protocol!"],
            e.exception.messages
        )

    def test_invitation_with_project_and_protocol(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
            protocol=self.protocol1,
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["You cannot select project and protocol for the same invitation!"],
            e.exception.messages
        )

    def test_invitation_inviter_cannot_invite_to_project(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher2,
            project=self.project1,
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["You cannot invite researchers to this project"],
            e.exception.messages
        )

    def test_invitation_inviter_cannot_invite_to_protocol(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher1,
            protocol=self.protocol1,
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["You cannot invite researchers to this protocol"],
            e.exception.messages
        )

    def test_invitation_with_the_same_inviter_and_invited(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher1,
            invited=self.researcher1,
            project=self.project1
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["Inviter and invited cannot be the same"],
            e.exception.messages
        )

    def test_accepted_invitation_without_invited(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
            accepted=True
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["Invited cannot be present for invitation that is not accepted"],
            e.exception.messages
        )

    def test_invitation_invited_already_in_project(self):
        invitation = Invitation(
            email='user2@gmail.com',
            inviter=self.researcher1,
            invited=self.researcher2,
            project=self.project1
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["Invited is already a participant for the selected project"],
            e.exception.messages
        )

    def test_invitation_invited_already_in_project(self):
        invitation = Invitation(
            email='user2@gmail.com',
            inviter=self.researcher2,
            invited=self.researcher1,
            protocol=self.protocol1
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["Invited is already a participant for the selected protocol"],
            e.exception.messages
        )

    def test_invitation_invited_already_in_project(self):
        invitation = Invitation(
            email='test@gmail.com',
            inviter=self.researcher1,
            invited=self.researcher3,
            project=self.project1
        )
        with self.assertRaises(ValidationError) as e:
            invitation.clean()
        self.assertEqual(
            ["Selected email address and the email address of the invited cannot be different"],
            e.exception.messages
        )

    def test_accept_invitation(self):
        invitation = Invitation.objects.create(
            email='user1@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
            role='contributor'
        )
        invitation.accept(self.researcher3)
        self.assertTrue(invitation.accepted)
        role = Role.objects.filter(
            researcher=self.researcher3,
            project=self.project1,
            role='contributor'
        )
        self.assertTrue(role.exists())

    def test_expired(self):
        invitation = Invitation.objects.create(
            email='user1@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
            expiration_days=3
        )
        invitation.datetime_created -= timezone.timedelta(3)
        self.assertTrue(invitation.is_expired())

    def test_not_expired(self):
        invitation = Invitation.objects.create(
            email='user1@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
            expiration_days=4
        )
        invitation.datetime_created -= timezone.timedelta(3)
        invitation.save()
        self.assertFalse(invitation.is_expired())

    def test_get_accept_invitation(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation') + '?key=' + invitation.key
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_accept_invitation_does_not_exist(self):
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation') + '?key=does_not_exist'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_accept_expired_invitation(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        invitation.datetime_created -= timezone.timedelta(3)
        invitation.save()
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation') + '?key=' + invitation.key
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_accept_invitation(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation')
        response = self.client.post(url, {'key': invitation.key})
        self.assertRedirects(response, '/projects/0f570c02/')


class InvitationsAjaxTests(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols',
    ]

    def setUp(self):
        self.client = Client()
        self.researcher1 = Researcher.objects.get(id=1)
        self.project1 = Project.objects.get(id=1)

    def test_get_create_invitation_no_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_invitation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_create_invitation_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_invitation')
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_post_create_invitation_empty(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_invitation')
        response = self.client.post(
            url,
            data={},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 400)

    def test_post_create_invitation(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_invitation')
        data = {
            'email': 'user3@gmail.com',
            'invitation_object': 'project',
            'object_choice': '0f570c02'
        }
        response = self.client.post(
            url,
            data=data,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        invitation = Invitation.objects.filter(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1
        )
        self.assertTrue(invitation.exists())


class InvitationsFormsTests(TestCase):
    fixtures = [
        'researchers/fixtures/users',
        'researchers/fixtures/researchers',
        'researchers/fixtures/universities',
        'researchers/fixtures/sources',
        'researchers/fixtures/roles',
        'projects/fixtures/projects',
        'protocols/fixtures/protocols',
    ]

    def setUp(self):
        self.researcher1 = Researcher.objects.get(id=1)
        self.researcher2 = Researcher.objects.get(id=2)
        self.researcher3 = Researcher.objects.get(id=3)
        self.project1 = Project.objects.get(id=1)
        self.protocol1 = Protocol.objects.get(id=1)

    def test_create_invitation_form_empty(self):
        form = CreateInvitationForm(data={}, inviter=self.researcher1)
        self.assertFalse(form.is_valid())

    def test_create_invitation_form_all_fields(self):
        data = {
            'email': 'user3@gmail.com',
            'invitation_object': 'project',
            'object_choice': '0f570c02'
        }
        form = CreateInvitationForm(data=data, inviter=self.researcher1)
        self.assertTrue(form.is_valid())

    def test_create_invitation_form_projects_queryset(self):
        data = {
            'email': 'user3@gmail.com',
            'invitation_object': 'project',
            'object_choice': '0f570c02'
        }
        form = CreateInvitationForm(data=data, inviter=self.researcher1)
        expected_projects = [
            Project.objects.get(id=1),
            Project.objects.get(id=2),
            Project.objects.get(id=3),
        ]
        projects = list(form.fields['object_choice'].queryset)
        self.assertEqual(projects, expected_projects)

    def test_create_invitation_form_protocols_queryset(self):
        data = {
            'email': 'user3@gmail.com',
            'invitation_object': 'protocol',
            'object_choice': '3e39fed1'
        }
        form = CreateInvitationForm(data=data, inviter=self.researcher1)
        expected_protocols = [
            Protocol.objects.get(id=3),
            Protocol.objects.get(id=6),
            Protocol.objects.get(id=8),
            Protocol.objects.get(id=10),
        ]
        protocols = list(form.fields['object_choice'].queryset)
        self.assertEqual(protocols, expected_protocols)
