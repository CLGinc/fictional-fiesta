from django import forms

from .models import Invitation
from projects.models import Project


class CreateInvitationModelForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = [
            'email',
            'inviter',
            'protocol',
            'project',
            ]


class CreateInvitationForm(forms.Form):
    INVITATION_FOR = (
        ('project', 'Project'),
        ('protocol', 'Protocol')
    )
    email = forms.EmailField()
    invitation_object = forms.ChoiceField(choices=INVITATION_FOR)
    object_choice = forms.ModelChoiceField(
        queryset=None,
        to_field_name='unique_id')

    def __init__(self, *args, **kwargs):
        self.inviter = kwargs.pop('inviter')
        super(CreateInvitationForm, self).__init__(*args, **kwargs)
        if self.data.get('invitation_object') == 'project':
            projects_to_edit = self.inviter.get_projects_to_edit()
            self.fields.get('object_choice').queryset = projects_to_edit
        elif self.data.get('invitation_object') == 'protocol':
            protocols_to_edit = self.inviter.get_protocols_to_edit()
            self.fields.get('object_choice').queryset = protocols_to_edit


class AcceptInvitationForm(forms.Form):
    key = forms.CharField(max_length=64)
