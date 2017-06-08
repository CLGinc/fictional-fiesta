from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import Role
from .models import Project


@receiver(post_save, sender=Project)
def create_owner_role(sender, instance, created, **kwargs):
    if created and not(kwargs.get('raw', False)) and hasattr(instance, '_owner'):
        Role.objects.create(
            user=instance._owner,
            protocol=instance,
            role='owner'
        )
