from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


class Source(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='sources')
    url = models.URLField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    sources = models.ManyToManyField(Source, related_name='projects', blank=True)
    protocols = models.ManyToManyField('protocols.Protocol', related_name='projects', blank=True)

    def __str__(self):
        return self.name


class Role(models.Model):
    ROLES = (
        ('owner', 'Owner'),
        ('contributor', 'Contributor'),
        ('watcher', 'Watcher'),
    )

    user = models.ForeignKey(User, related_name='roles')
    project = models.ForeignKey(Project, related_name='roles', null=True, blank=True)
    protocol = models.ForeignKey('protocols.Protocol', related_name='roles', null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLES)

    class Meta:
        unique_together = (('user', 'project'), ('user', 'protocol'))

    def __str__(self):
        role_object_label = ''
        if self.project:
            role_object_label = 'project {}'.format(self.project.name)
        elif self.protocol:
            role_object_label = 'protocol {}'.format(self.protocol.name)
        return '{} {} of/to {}'.format(
            self.user.username,
            self.get_role_display(),
            role_object_label
        )

    def clean(self):
        if not(self.project or self.protocol):
            raise ValidationError('You must choose either project or protocol!')
        if self.project and self.protocol:
            raise ValidationError('You cannot select project and protocol for the same role!')
