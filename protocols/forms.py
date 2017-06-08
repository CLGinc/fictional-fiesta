from django import forms

from users.models import Role
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
        self.user = kwargs.pop('user')
        super(BasicProtocolForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance._user = self.user
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
            'data_type_independent',
            'dependent_variable',
            'data_type_dependent',
            'protocol',
            'data_columns',
            'project',
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        protocol = kwargs.pop('protocol')
        super(BasicResultForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = None
        self.fields['project'].queryset = Project.objects.filter(
            protocols__in=[protocol],
            roles__role__in=Role.ROLES_CAN_EDIT,
            roles__user=user
        )
