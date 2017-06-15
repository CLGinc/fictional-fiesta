from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import m2m_changed

from users.models import Role
from protocols.models import Protocol
from .models import Project


@receiver(post_save, sender=Project)
def create_owner_role(sender, instance, created, **kwargs):
    if created and not(kwargs.get('raw', False)) and hasattr(instance, '_owner'):
        Role.objects.create(
            user=instance._owner,
            project=instance,
            role='owner'
        )


@receiver(m2m_changed, sender=Project.protocols.through)
def create_roles_on_add_protocol(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        roles_added_protocol = dict(Role.ROLES_ADDED_PROTOCOL)
        added_protocols = Protocol.objects.filter(pk__in=pk_set)
        roles = instance.roles.all()
        for role in roles:
            protocols_to_create_roles = added_protocols.exclude(
                roles__user=role.user
            )
            for protocol in protocols_to_create_roles:
                Role.objects.create(
                    user=role.user,
                    protocol=protocol,
                    role=roles_added_protocol.get(role.role, role.role)
                )
