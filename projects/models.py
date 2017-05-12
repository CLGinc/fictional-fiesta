import uuid

from django.db import models
from django.apps import apps


class Project(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True)
    sources = models.ManyToManyField(
        'researchers.Source',
        related_name='projects',
        blank=True)
    protocols = models.ManyToManyField(
        'protocols.Protocol',
        related_name='projects',
        blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-datetime_created']

    def __str__(self):
        return self.name

    def get_participants_by_role(self):
        participants_by_role = list()
        RoleModel = apps.get_model('researchers', 'Role')
        for role_value, role_label in RoleModel.ROLES:
            if self.roles.filter(role=role_value).exists():
                participants_by_role.append(
                    (
                        role_label,
                        self.roles.filter(
                            role=role_value).order_by('researcher')
                    )
                )
        return participants_by_role
