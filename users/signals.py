from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Role


@receiver(post_save, sender=User)
def assign_invitations(sender, created, instance, raw, using, update_fields, **kwargs):
    if not raw and created:
        instance.assign_invitations()


@receiver(post_save, sender=Role)
def create_project_protocols_roles(sender, created, instance, raw, using, update_fields, **kwargs):
    '''
    When a project role is created this method creates roles for all
    protocols that belong to that project with the new user.
    The role is the same.
    '''
    if not raw and created and \
            instance.project is not None and instance.role != 'owner':
        protocols = instance.project.protocols.exclude(
            roles__user=instance.user
        )
        for protocol in protocols:
            Role.objects.create(
                user=instance.user,
                protocol=protocol,
                role=instance.role
            )
