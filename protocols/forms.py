from django import forms
from django.forms.models import inlineformset_factory

from researchers.models import Role
from.models import Protocol, Procedure, Step


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
