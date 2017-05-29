from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Researcher


@receiver(post_save, sender=User)
def set_created_users_inactive(sender, instance, created, **kwargs):
    if created and not(kwargs.get('raw', False)):
        Researcher.objects.create(user=instance)
