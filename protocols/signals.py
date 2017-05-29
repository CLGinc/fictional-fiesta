from django.db.models.signals import post_save
from django.dispatch import receiver

from researchers.models import Role
from .models import Protocol


@receiver(post_save, sender=Protocol)
def create_researcher(sender, instance, created, **kwargs):
    if created and not(kwargs.get('raw', False)) and hasattr(instance, '_researcher'):
        Role.objects.create(
            researcher=instance._researcher,
            protocol=instance,
            role='owner'
        )
