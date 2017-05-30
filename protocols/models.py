import uuid

from django.apps import apps

from django.contrib.postgres.fields import JSONField
from django.db import models
from django.core.exceptions import ValidationError

from .json_validators import vaidate_result_data_columns
from .json_validators import vaidate_protocol_procedure


class Asset(models.Model):
    CATEGORIES = (
        ('material', 'Material'),
        ('equipment', 'Equipment')
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORIES)

    def __str__(self):
        return self.name


class Protocol(models.Model):
    LABELS = (
        ('standard', 'Standard'),
        ('modified', 'Modified'),
    )
    DEFAULT_LABEL = 'standard'

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1024, blank=True)
    label = models.CharField(max_length=20, default=DEFAULT_LABEL, choices=LABELS)
    assets = models.ManyToManyField(
        Asset,
        related_name='protocols',
        blank=True)
    sources = models.ManyToManyField(
        'researchers.Source',
        related_name='protocols',
        blank=True)
    procedure = JSONField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        'researchers.Researcher',
        related_name='procedures')

    class Meta:
            ordering = ['-datetime_created']

    def __str__(self):
        return self.name

    def clean(self):
        if hasattr(self, 'procedure'):
            vaidate_protocol_procedure(
                value=self.procedure,
                field_name='procedure'
            )

    def get_owner(self):
        return self.roles.get(role='owner').researcher

    def get_assets_by_category(self):
        assets_by_category = list()
        for category_value, category_label in Asset.CATEGORIES:
            if self.assets.filter(category=category_value).exists():
                assets_by_category.append(
                    (
                        category_label,
                        self.assets.filter(category=category_value)
                    )
                )
        return assets_by_category

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


class Result(models.Model):
    STATES = (
        ('created', 'Created'),
        ('finished', 'Finished'),
    )
    DATA_TYPES = (
        ('number', 'Number'),
        ('string', 'Text'),
        ('boolean', 'Yes/No'),
    )

    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    title = models.CharField(max_length=255)
    note = models.CharField(max_length=255, null=True, blank=True)
    owner = models.ForeignKey('researchers.Researcher', related_name='results')
    state = models.CharField(
        max_length=20,
        choices=STATES,
        default=STATES[0][0]
    )
    is_successful = models.BooleanField(default=False)
    protocol = models.ForeignKey(Protocol, related_name='results')
    project = models.ForeignKey(
        'projects.Project',
        related_name='results',
        null=True,
        blank=True
    )
    independent_variable = models.CharField(max_length=255)
    dependent_variable = models.CharField(max_length=255)
    data_type = models.CharField(
        max_length=20,
        choices=DATA_TYPES,
        default=DATA_TYPES[0][0]
    )
    data_columns = JSONField()
    datetime_created = models.DateTimeField(auto_now_add=True)

    class Meta:
            ordering = ['-datetime_created', 'owner']

    def __str__(self):
        return 'Result for protocol {} owned by {}'.format(self.protocol, self.owner)

    def clean(self):
        RoleModel = apps.get_model('researchers', 'Role')
        if hasattr(self, 'owner') and hasattr(self, 'protocol'):
            if not(self.protocol.roles.filter(researcher=self.owner, role__in=RoleModel.ROLES_CAN_EDIT).exists()):
                raise ValidationError({'owner': 'The selected researcher cannot add results to this protocol!'})
        if self.is_successful and not(self.state == 'finished'):
            raise ValidationError({'is_successful': 'Unfinished result cannot be marked successful!'})
        if self.project:
            if not(self.protocol in self.project.protocols.all()):
                raise ValidationError('The selected protocol does not belong to the selected project!')
            if not(self.project.roles.filter(researcher=self.owner, role__in=RoleModel.ROLES_CAN_EDIT).exists()):
                raise ValidationError({'owner': 'The selected researcher cannot add results to this project!'})
        if hasattr(self, 'data_columns') and hasattr(self, 'data_type'):
            vaidate_result_data_columns(
                value=self.data_columns,
                data_type=self.data_type,
                field_name='data_columns'
            )


class Attachment(models.Model):
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    description = models.CharField(max_length=255, null=True, blank=True)
    result = models.ForeignKey(Result, related_name='attachemnts')

    def __str__(self):
        return self.file.filename
