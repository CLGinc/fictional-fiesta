from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Role
from .models import Protocol


@receiver(post_save, sender=Protocol)
def create_user(sender, instance, created, **kwargs):
    if created and not(kwargs.get('raw', False)) and hasattr(instance, '_user'):
        Role.objects.create(
            user=instance._user,
            protocol=instance,
            role='owner'
        )
