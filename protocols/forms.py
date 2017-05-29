from django import forms
from django.forms.models import inlineformset_factory

from researchers.models import Role
from projects.models import Project
from.models import Protocol, Procedure, Step, Result


StepsFormset = inlineformset_factory(
    parent_model=Procedure,
    model=Step,
    fields=('title', 'text', 'order'),
    extra=0,
    max_num=64,
    min_num=1
)


class BasicProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = [
            'name',
            'description',
            'label'
        ]

    def __init__(self, *args, **kwargs):
        self.researcher = kwargs.pop('researcher')
        super(BasicProtocolForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(BasicProtocolForm, self).save(commit=commit)
        if not(
                Role.objects.filter(
                    role='owner',
                    protocol=instance
                ).exists() or
                Role.objects.filter(
                    researcher=self.researcher,
                    protocol=instance
                ).exists()):
            Role.objects.create(
                researcher=self.researcher,
                protocol=instance,
                role='owner'
            )
        if not(Procedure.objects.filter(protocol=instance).exists()):
            Procedure.objects.create(
                protocol=instance,
                last_modified_by=self.researcher
            )
        return instance


class BasicResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = [
            'title',
            'note',
            'owner',
            'state',
            'is_successful',
            'independent_variable',
            'dependent_variable',
            'protocol',
            'data_columns',
            'project',
        ]

    def __init__(self, *args, **kwargs):
        researcher = kwargs.pop('researcher')
        protocol = kwargs.pop('protocol')
        super(BasicResultForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = None
        self.fields['project'].queryset = Project.objects.filter(
            protocols__in=[protocol],
            roles__role__in=Role.ROLES_CAN_EDIT,
            roles__researcher=researcher
        )
