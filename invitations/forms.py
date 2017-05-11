from django import forms

from .models import Invitation


class CreateInvitationModelForm(forms.ModelForm):
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
