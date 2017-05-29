from django import forms

from researchers.models import Role
from projects.models import Project
from.models import Protocol, Result


class BasicProtocolForm(forms.ModelForm):
    class Meta:
        model = Protocol
        fields = [
            'name',
            'description',
            'label',
            'procedure',
            'last_modified_by',
        ]

    def __init__(self, *args, **kwargs):
        self.researcher = kwargs.pop('researcher')
        super(BasicProtocolForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance._researcher = self.researcher
        instance = super(BasicProtocolForm, self).save(commit=commit)
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
