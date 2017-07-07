from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Invitation
from users.models import Role
from SciLog.mail import MJEmailMessage


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
            "invited": str(instance.invited or instance.email),
            "inviter": str(instance.inviter),
            "object": {
                "type": instance.get_item(),
                "name": instance.get_item_name()
            },
            "role": instance.role,
            "url": reverse('invitations:invitations_list')
        }
        email = MJEmailMessage(
            subject='',
            body='',
            to=[instance.email],
            from_email=settings.MJ_INVITATION_FROM,
            template_id=settings.MJ_INVITATION_TEMPLATE_ID,
            variables=variables
        )
        email.send(fail_silently=settings.DEBUG)


@receiver(post_save, sender=Invitation)
def create_role(sender, created, instance, raw, using, update_fields, **kwargs):
    if not raw and instance.invited and instance.accepted:
        if instance.project is not None:
            Role.objects.get_or_create(
                user=instance.invited,
                role=instance.role,
                project=instance.project
            )
        elif instance.protocol is not None:
            Role.objects.get_or_create(
                user=instance.invited,
                role=instance.role,
                protocol=instance.protocol
            )
