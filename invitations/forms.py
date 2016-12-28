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


class AcceptInvitationForm(forms.Form):
    key = forms.CharField(max_length=64)
