from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.test.client import Client
from django.core.urlresolvers import reverse

from .models import Invitation
from .forms import CreateInvitationModelForm
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
        self.project1 = Project.objects.get(name='Project 1')
        self.protocol1 = Protocol.objects.get(name='Protocol 1')

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

    def test_invitation_invited_already_in_protocol(self):
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

    def test_invitation_invited_different_email(self):
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

    def test_get_invitations_list(self):
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('invitations_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_item_project(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.assertEqual(invitation.get_item(), 'Project')

    def test_get_item_name_project(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.assertEqual(invitation.get_item_name(), 'Project 1')

    def test_get_item_protocol(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher2,
            protocol=self.protocol1,
        )
        self.assertEqual(invitation.get_item(), 'Protocol')

    def test_get_item_name_protocol(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher2,
            protocol=self.protocol1,
        )
        self.assertEqual(invitation.get_item_name(), 'Protocol 1')

    def test_get_assign_invitation(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('assign_invitation', kwargs={'uuid': invitation.uuid})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('invitations_list'))
        invitation.refresh_from_db()
        self.assertEqual(invitation.invited, self.researcher3)

    def test_get_assign_invitation_404(self):
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('assign_invitation', kwargs={'uuid': '74369692-6844-430d-bff2-90904fc3094e'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


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
        self.project1 = Project.objects.get(name='Project 1')

    def test_get_create_invitation_no_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_invitation')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_get_create_invitation_ajax(self):
        self.client.login(username='user1@gmail.com', password='user1')
        url = reverse('create_invitation')
        response = self.client.get(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 405)

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
            'project': '808d85c6-8fdb-478d-994a-aab8496ef4cb',
            'role': 'watcher'
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

    def test_get_accept_invitation_no_ajax(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation', kwargs={'uuid': invitation.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 405)

    def test_post_accept_invitation_no_ajax(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation', kwargs={'uuid': invitation.uuid})
        response = self.client.post(
            url,
            {'uuid': invitation.uuid},
        )
        self.assertEqual(response.status_code, 403)

    def test_get_accept_invitation_ajax(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation', kwargs={'uuid': invitation.uuid})
        response = self.client.get(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 405)

    def test_post_accept_expired_invitation_ajax(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        invitation.datetime_created -= timezone.timedelta(3)
        invitation.save()
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation', kwargs={'uuid': invitation.uuid})
        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_post_accept_invitation(self):
        invitation = Invitation.objects.create(
            email='user3@gmail.com',
            inviter=self.researcher1,
            project=self.project1,
        )
        self.client.login(username='user3@gmail.com', password='user3')
        url = reverse('accept_invitation', kwargs={'uuid': invitation.uuid})
        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)


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
        self.project1 = Project.objects.get(name='Project 1')
        self.project2 = Project.objects.get(name='Project 2')
        self.project3 = Project.objects.get(name='Project 3')
        self.protocol1 = Protocol.objects.get(name='Protocol 1')
        self.protocol3 = Protocol.objects.get(name='Protocol 3')
        self.protocol6 = Protocol.objects.get(name='Protocol 6')
        self.protocol8 = Protocol.objects.get(name='Protocol 8')
        self.protocol10 = Protocol.objects.get(name='Protocol 10')

    def test_create_invitation_form_empty(self):
        form = CreateInvitationModelForm(data={})
        self.assertFalse(form.is_valid())

    def test_create_invitation_form_all_fields(self):
        data = {
            'email': 'user3@gmail.com',
            'project': '808d85c6-8fdb-478d-994a-aab8496ef4cb',
            'inviter': self.researcher1.pk
        }
        form = CreateInvitationModelForm(data=data)
        self.assertTrue(form.is_valid())

    def test_create_invitation_form_projects_queryset(self):
        data = {
            'email': 'user3@gmail.com',
            'project': '808d85c6-8fdb-478d-994a-aab8496ef4cb',
            'inviter': self.researcher1.pk
        }
        form = CreateInvitationModelForm(data=data)
        expected_projects = [
            self.project1,
            self.project2,
            self.project3,
        ]
        projects = list(form.fields['project'].queryset)
        self.assertEqual(projects, expected_projects)

    def test_create_invitation_form_protocols_queryset(self):
        data = {
            'email': 'user3@gmail.com',
            'protocol': '7e453405-5bfe-4ef7-86ba-121ae89c6510',
            'inviter': self.researcher1.pk
        }
        form = CreateInvitationModelForm(data=data)
        expected_protocols = [
            self.protocol3,
            self.protocol6,
            self.protocol8,
            self.protocol10,
        ]
        protocols = list(form.fields['protocol'].queryset)
        self.assertEqual(protocols, expected_protocols)
