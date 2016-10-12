from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.db import models

from adminsortable.models import SortableMixin


class Asset(models.Model):
    CATEGORIES = (
        ('matirial', 'Material'),
        ('equipment', 'Equipment')
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORIES)

    def __str__(self):
        return self.name


class Procedure(models.Model):
    datetime_last_modified = models.DateTimeField(auto_now=True)
    last_modified_by_user = models.ForeignKey(User, related_name='procedures')

    def __str__(self):
        return 'Procedure {} created by {}'.format(self.id, self.last_modified_by_user)


class Protocol(models.Model):
    LABELS = (
        ('standard', 'Standard'),
        ('modified', 'Modified'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    label = models.CharField(max_length=20, choices=LABELS)
    assets = models.ManyToManyField(Asset, related_name='protocols')
    procedure = models.OneToOneField(Procedure, related_name='protocol')
    sources = models.ManyToManyField('projects.Source', related_name='protocols', blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Step(SortableMixin):
    name = models.CharField(max_length=255)
    procedure = models.ForeignKey(Procedure, related_name='steps')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class Result(models.Model):
    STATES = (
        ('created', 'Created'),
        ('finished', 'Finished'),
    )

    note = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey(User, related_name='results')
    state = models.CharField(max_length=20, choices=STATES, default=STATES[0][0])

    def __str__(self):
        return 'Result {}'.format(self.id)


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    description = models.CharField(max_length=255, null=True, blank=True)
    result = models.ForeignKey(Result, related_name='attachemnts')

    def __str__(self):
        return self.file.filename


class DataColumn(models.Model):
    data = JSONField()
    is_independent = models.BooleanField(default=False)
    measurement = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def __str__(self):
        independent_label = '[independent] ' if self.is_independent else ''
        return '{}{}'.format(independent_label, self.measurement)
