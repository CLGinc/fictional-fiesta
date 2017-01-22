from django import forms

from .models import Invitation
from projects.models import Project
from researchers.models import Researcher, Role


class CreateInvitationModelForm(forms.ModelForm):
    role = forms.ChoiceField(choices=Role.ROLES_TO_INVITE, required=False)

    class Meta:
        model = Invitation
        fields = [
            'email',
            'inviter',
            'invited',
            'protocol',
            'project',
            'role',
            ]


class CreateInvitationForm(forms.Form):
    INVITATION_FOR = (
        ('project', 'Project'),
        ('protocol', 'Protocol')
    )
    email = forms.EmailField()
    role = forms.ChoiceField(choices=Role.ROLES_TO_INVITE, required=False)
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

    def get_invited(self):
        if self.cleaned_data:
            if Researcher.objects.filter(
                user__email=self.cleaned_data.get('email')
            ).exists():
                return Researcher.objects.get(
                    user__email=self.cleaned_data.get('email')
                )


class AcceptInvitationForm(forms.Form):
    key = forms.CharField(max_length=64)
