from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User


@receiver(post_save, sender=User)
def assign_invitations(sender, created, instance, raw, using, update_fields, **kwargs):
    if not raw and created:
        instance.assign_invitations()
