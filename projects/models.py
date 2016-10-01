from django.contrib.auth.models import User
from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name='sources')
    url = models.URLField(max_length=255, null=True, blank=True)
    isbn = models.CharField(max_length=255, null=True, blank=True)


class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    sources = models.ManyToManyField(Source, related_name='projects')
    protocols = models.ManyToManyField('protocols.Protocol', related_name='projects')


class Role(models.Model):
    ROLES = (
        ('owner', 'Owner'),
        ('contributor', 'Contributor'),
        ('watcher', 'Watcher'),
    )

    user = models.ForeignKey(User, related_name='roles')
    project = models.ForeignKey(Project, related_name='roles')
    protocol = models.ForeignKey('protocols.Protocol', related_name='roles')
    role = models.CharField(max_length=255, choices=ROLES)
