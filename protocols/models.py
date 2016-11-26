import os

from adminsortable.models import SortableMixin

from django.contrib.postgres.fields import JSONField
from django.db import models


def create_unique_id():
    unique_id = os.urandom(4).hex()
    while(True):
        try:
            Protocol.objects.get(unique_id=unique_id)
        except Protocol.DoesNotExist:
            return(unique_id)
        unique_id = os.urandom(4).hex()


class Asset(models.Model):
    CATEGORIES = (
        ('material', 'Material'),
        ('equipment', 'Equipment')
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORIES)

    def __str__(self):
        return self.name


class Procedure(models.Model):
    datetime_last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey('researchers.Researcher', related_name='procedures')

    def __str__(self):
        return 'Procedure {} created by {}'.format(self.id, self.last_modified_by)


class Protocol(models.Model):
    LABELS = (
        ('standard', 'Standard'),
        ('modified', 'Modified'),
    )

    unique_id = models.CharField(max_length=8, unique=True, default=create_unique_id)
    name = models.CharField(max_length=255)
    description = models.TextField()
    label = models.CharField(max_length=20, choices=LABELS)
    assets = models.ManyToManyField(Asset, related_name='protocols')
    procedure = models.OneToOneField(Procedure, related_name='protocol')
    sources = models.ManyToManyField('researchers.Source', related_name='protocols', blank=True)
    datetime_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_owner(self):
        return self.roles.get(role='owner')


class Step(SortableMixin):
    text = models.CharField(max_length=255)
    procedure = models.ForeignKey(Procedure, related_name='steps')
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class Result(models.Model):
    STATES = (
        ('created', 'Created'),
        ('finished', 'Finished'),
    )

    note = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey('researchers.Researcher', related_name='results')
    state = models.CharField(max_length=20, choices=STATES, default=STATES[0][0])
    is_successful = models.BooleanField(default=False)
    protocol = models.ForeignKey(Protocol, related_name='results')
    project = models.ForeignKey('projects.Project', related_name='results', null=True, blank=True)

    def __str__(self):
        return 'Result {}'.format(self.id)


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    description = models.CharField(max_length=255, null=True, blank=True)
    result = models.ForeignKey(Result, related_name='attachemnts')

    def __str__(self):
        return self.file.filename


class DataColumn(models.Model):
    result = models.ForeignKey(Result, related_name='data_columns')
    data = JSONField()
    is_independent = models.BooleanField(default=False)
    measurement = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)

    def __str__(self):
        independent_label = '[independent] ' if self.is_independent else ''
        return '{}{}'.format(independent_label, self.measurement)
