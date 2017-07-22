from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.apps import apps

from protocols.models import Protocol
from SciLog.mail import MJEmailMessage


class Role(models.Model):
    ROLES_ADDED_PROTOCOL = (
        ('owner', 'contributor'),
    )
    ROLES = (
        ('owner', 'Owner'),
        ('contributor', 'Contributor'),
        ('watcher', 'Watcher'),
    )
    ROLES_CAN_EDIT = (
        'owner',
    )
    ROLES_CAN_ADD_ITEMS = (
        'owner',
        'contributor'
    )
    ROLES_CAN_INVITE = (
        'owner',
    )
    ROLES_TO_INVITE = (
        ('contributor', 'Contributor'),
        ('watcher', 'Watcher'),
    )
    DEFAULT_INVITATION_ROLE = ('watcher', 'Watcher')

    user = models.ForeignKey('User', related_name='roles')
    project = models.ForeignKey(
        'projects.Project',
        related_name='roles',
        null=True,
        blank=True)
    protocol = models.ForeignKey(
        'protocols.Protocol',
        related_name='roles',
        null=True,
        blank=True)
    role = models.CharField(max_length=255, choices=ROLES)

    class Meta:
        unique_together = (
            ('user', 'project'),
            ('user', 'protocol'))

    def __str__(self):
        role_object_label = ''
        if self.project:
            role_object_label = 'project {}'.format(self.project.name)
        elif self.protocol:
            role_object_label = 'protocol {}'.format(self.protocol.name)
        return '{} {} of/to {}'.format(
            self.user.username,
            self.get_role_display(),
            role_object_label
        )

    def clean(self):
        if not(self.project or self.protocol):
            raise ValidationError('You must choose \
either project or protocol!')
        if self.project and self.protocol:
            raise ValidationError('You cannot select \
project and protocol for the same role!')
        if self.role == 'owner':
            if self.project and \
                    self.project.roles.filter(role='owner').exclude(
                        pk=self.pk
                    ).exists():
                raise ValidationError('There is already \
an owner of this project!')
            if self.protocol and \
                    self.protocol.roles.filter(role='owner').exclude(
                        pk=self.pk
                    ).exists():
                raise ValidationError('There is already \
an owner of this protocol!')

    @classmethod
    def get_db_roles(cls):
        return [role[0] for role in cls.ROLES]


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email address'
    )
    scientific_degree = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.first_name, self.last_name)
        else:
            return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_roles(self, scope=None, roles=Role.get_db_roles()):
        """
        Returns roles list django query set based on
        scope and a list of role names.
        If no role names are specified all roles are selected.
        Scope defines if the query gets roles for projects, protocols or both.
        """
        if scope == 'project':
            return Role.objects.filter(
                user=self,
                role__in=roles,
                protocol=None
            ).exclude(project=None).select_related(scope)
        elif scope == 'protocol':
            return Role.objects.filter(
                user=self,
                role__in=roles,
                project=None
            ).exclude(protocol=None).select_related(scope)
        else:
            return Role.objects.filter(
                user=self,
                role__in=roles,).select_related('project', 'protocol')

    def get_protocols_to_add(self, project):
        if self.can_add_items(project):
            protocols = Protocol.objects.filter(
                roles__user=self,
                roles__project=None,
                roles__role__in=Role.ROLES_CAN_ADD_ITEMS
            ).exclude(uuid__in=project.protocols.all())
            return protocols
        else:
            return Protocol.objects.none()

    def get_sources_to_add(self, project):
        if self.can_add_items(project):
            sources = self.sources.all().exclude(
                id__in=project.sources.all()
            )
            return sources
        else:
            return Source.objects.none()

    def can_update(self, item):
        role = item.roles.get(user=self)
        return role.role in Role.ROLES_CAN_EDIT

    def can_add_items(self, item):
        role = item.roles.get(user=self)
        return role.role in Role.ROLES_CAN_ADD_ITEMS

    def assign_invitations(self):
        InvitationModel = apps.get_model('invitations', 'Invitation')
        invitations = InvitationModel.objects.filter(
            email=self.email, invited=None
        )
        if invitations.exists():
            for invitation in invitations:
                invitation.invited = self
                invitation.save()

    def email_user(
            self,
            template_id,
            variables,
            from_email=None,
            fail_silently=False,
            **kwargs):
        msg = MJEmailMessage(
            subject=kwargs.pop('subject', ''),
            body=kwargs.pop('body', ''),
            to=[self.email],
            from_email=from_email,
            template_id=template_id,
            variables=variables,
            **kwargs
        )
        msg.send(fail_silently=fail_silently)

    def get_invitations(self, **kwargs):
        InvitationModel = apps.get_model('invitations', 'Invitation')
        return InvitationModel.objects.filter(**kwargs, invited=self)


class Source(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='sources')
    url = models.URLField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name
