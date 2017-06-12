from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse
import json

from .models import Invitation
from users.models import Role


@receiver(pre_save, sender=Invitation)
def set_invited(sender, instance, raw, using, update_fields, **kwargs):
    if not (raw or instance.invited):
        invited = instance.get_invited()
        if invited:
            instance.invited = invited


@receiver(post_save, sender=Invitation)
def send_mail(sender, created, instance, raw, using, update_fields, **kwargs):
    if not raw and created:
        variables = {
            "invited": str(instance.invited),
            "inviter": str(instance.inviter),
            "object": {
                "type": instance.get_item(),
                "name": instance.get_item_name()
            },
            "role": instance.role,
            "url": reverse('invitations_list')
        }
        instance.invited.email_user(
            template_id=settings.MJ_INVITATION_TEMPLATE_ID,
            variables=json.dumps(variables),
            from_email=settings.MJ_INVITATION_FROM,
            fail_silently=settings.DEBUG
        )


@receiver(post_save, sender=Invitation)
def create_role(sender, created, instance, raw, using, update_fields, **kwargs):
    if not raw and instance.invited and instance.accepted:
        if instance.project and not Role.objects.filter(
            user=instance.invited,
            project=instance.project
        ).exists():
            role = Role(
                user=instance.invited,
                role=instance.role,
                project=instance.project
            )
        elif instance.protocol and not Role.objects.filter(
            user=instance.invited,
            project=instance.project
        ).exists():
            role = Role(
                user=instance.invited,
                protocol=instance.protocol
            )
        role.save()
