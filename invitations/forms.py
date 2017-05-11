from django import forms

from .models import Invitation
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
        to_field_name='uuid')

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

    def get_data_for_model_form(self, researcher):
        data = {}
        if self.cleaned_data:
            data = {
                'email': self.cleaned_data.get('email'),
                'inviter': researcher.id,
            }
            invited = self.get_invited()
            if invited:
                data['invited'] = invited.id
            if self.cleaned_data.get('role'):
                data['role'] = self.cleaned_data.get('role')
            if self.cleaned_data.get('invitation_object') == 'project':
                data['project'] = self.cleaned_data.get('object_choice').id
            elif self.cleaned_data.get('invitation_object') == 'protocol':
                data['protocol'] = self.cleaned_data.get('object_choice').id
        return data
