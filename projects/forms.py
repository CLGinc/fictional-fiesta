from django import forms

from .models import Project


class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


class AddElementsForm(forms.Form):
    def __init__(self, *args, **kwargs):
            queryset = kwargs.pop('queryset')
            super(AddElementsForm, self).__init__(*args, **kwargs)
            self.fields['element_choices'].queryset = queryset

    CHOICES = (
        ('p', 'Protocols'),
        ('s', 'Sources'))
    element_choices = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )
    element_type = forms.ChoiceField(CHOICES)
