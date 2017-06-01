from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Invitation


@receiver(pre_save, sender=Invitation)
def set_invited(sender, instance, raw, using, update_fields, **kwargs):
    if not (raw or instance.invited):
        invited = instance.get_invited()
        if invited:
            instance.invited = invited
