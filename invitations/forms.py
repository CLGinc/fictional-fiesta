from django import forms

from .models import Invitation


class CreateInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = [
            'email',
            'inviter',
            'protocol',
            'project',
            ]


class AcceptInvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = [
            'key',
            ]
