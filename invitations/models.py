from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

from .utils import generate_key

from researchers.models import Role


class Invitation(models.Model):
    DEFAULT_ROLE = 'watcher'

    email = models.EmailField(max_length=254)
    inviter = models.ForeignKey(
        'researchers.Researcher',
        related_name='inviter_invitations'
    )
    invited = models.ForeignKey(
        'researchers.Researcher',
        related_name='invited_invitations',
        blank=True,
        null=True
    )
    protocol = models.ForeignKey(
        'protocols.Protocol',
        related_name='invitations',
        blank=True,
        null=True
    )
    project = models.ForeignKey(
        'projects.Project',
        related_name='invitations',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=255,
        choices=Role.ROLES_TO_INVITE,
        default=DEFAULT_ROLE)
    key = models.CharField(
        unique=True,
        default=generate_key,
        max_length=64,
        editable=False)
    accepted = models.BooleanField(default=False)
    expiration_days = models.PositiveSmallIntegerField(default=3)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('email', 'project'),
            ('email', 'protocol'))

    def __str__(self):
        target = 'Project' if self.project else 'Protocol'
        invited = self.invited if self.invited else self.email
        return('{} invitiation from {} to {}'.format(
            target,
            self.inviter,
            invited
            )
        )

    def clean(self):
        if not(self.project or self.protocol):
            raise ValidationError('You must choose \
either project or protocol!')
        if self.project and self.protocol:
            raise ValidationError('You cannot select \
project and protocol for the same invitation!')
        if self.project and \
            self.inviter.roles.filter(
                project=self.project,
                role='watcher'):
            raise ValidationError('You cannot invite \
researchers to this project')
        if self.protocol and \
            self.inviter.roles.filter(
                protocol=self.protocol,
                role='watcher'):
            raise ValidationError('You cannot invite \
researchers to this protocol')
        if self.inviter == self.invited:
            raise ValidationError('Inviter \
and invited cannot be the same')
        if self.accepted and not(self.invited):
            raise ValidationError('Invited \
cannot be present for invitation that is not accepted')
        if self.invited and self.project:
            if self.project.roles.filter(researcher=self.invited):
                raise ValidationError('Invited is already a participant \
for the selected project')
        if self.invited and self.protocol:
            if self.protocol.roles.filter(researcher=self.invited):
                raise ValidationError('Invited is already a participant \
for the selected protocol')
        if self.invited:
            if self.invited.user.email != self.email:
                raise ValidationError('Selected email address and the \
email address of the invited cannot be different')

    def send(self):
        # To develop seinding via MJ send API
        pass

    def accept(self, invited):
        if not(self.is_expired()):
            if self.project:
                Role.objects.create(
                    researcher=invited,
                    role=self.role,
                    project=self.project
                )
            elif self.protocol:
                Role.objects.create(
                    researcher=invited,
                    role=self.role,
                    protocol=self.protocol
                )
            self.invited = invited
            self.accepted = True
            self.save()

    def is_expired(self):
        expiration_date = self.datetime_created + \
            timezone.timedelta(self.expiration_days)
        return not(expiration_date > timezone.now() > self.datetime_created)

    def can_be_accepted(self, accepting_researcher):
        if self.is_expired():
            return False
        if self.inviter == accepting_researcher:
            return False
        if self.invited and self.invited != accepting_researcher:
            return False
        if self.email != accepting_researcher.user.email:
            return False
        return True

    def get_item(self):
        if self.project:
            return 'Project'
        elif self.protocol:
            return 'Protocol'
        else:
            return None

    def get_item_name(self):
        if self.project:
            return self.project.name
        elif self.protocol:
            return self.protocol.name
        else:
            return None
