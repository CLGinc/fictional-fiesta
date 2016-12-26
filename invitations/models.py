import uuid


from django.db import models


class Invitation(models.Model):
    email = mdoels.EmailField(unique=True, max_length=254)
    inviter = models.ForeignKey(
        'researchers.Researcher',
        related_name='invitations'
    )
    invited = models.ForeignKey(
        'researchers.Researcher',
        related_name='invitations',
        blank=True,
        null=True
    )
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    expiration_days = models.PositiveSmallIntegerField(default=3)
    datetime_created = models.DateTimeField(auto_now_add=True)
