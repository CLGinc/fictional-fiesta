from django.utils.crypto import get_random_string
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


def generate_key():
    while(True):
        key = get_random_string(64)
        try:
            Invitation.objects.get(key=key)
        except Invitation.DoesNotExist:
            return(key)


class Invitation(models.Model):
    email = models.EmailField(unique=True, max_length=254)
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
    key = models.CharField(
        unique=True,
        default=generate_key,
        max_length=64,
        editable=False)
    accepted = models.BooleanField(default=False)
    expiration_days = models.PositiveSmallIntegerField(default=3)
    datetime_created = models.DateTimeField(auto_now_add=True)

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
                project=self.protocol,
                role='watcher'):
            raise ValidationError('You cannot invite \
researchers to this protocol')
        if self.inviter == self.invited:
            raise ValidationError('Inviter \
and invited cannot be the same')

    def send(self):
        # To develop seinding via MJ send API
        pass

    def accept(self, invited):
        self.invited = invited
        self.accepted = True
        self.save()

    def is_expired(self):
        expiration_date = self.datetime_created + \
            timezone.timedelta(self.expiration_days)
        return not(expiration_date > timezone.now() > self.datetime_created)
