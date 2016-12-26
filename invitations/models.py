from django.utils.crypto import get_random_string
from django.db import models


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
    expiration_days = models.PositiveSmallIntegerField(default=3)
    datetime_created = models.DateTimeField(auto_now_add=True)
