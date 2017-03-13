from django import forms

from researchers.models import Role
from.models import Protocol, Procedure


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
        Role.objects.create(
            researcher=self.researcher,
            protocol=instance,
            role='owner'
        )
        Procedure.objects.create(
            protocol=instance,
            last_modified_by=self.researcher
        )
        return instance
