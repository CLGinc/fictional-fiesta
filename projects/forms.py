from django import forms

from .models import Project


class BasicProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        if kwargs.get('user'):
            self.user = kwargs.pop('user')
        else:
            self.user = None
        super(BasicProjectForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        self.instance._owner = self.user
        instance = super(BasicProjectForm, self).save(commit=True)
        return instance


class AddElementsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        selected_project = kwargs.pop('selected_project')
        user = kwargs.pop('user')
        super(AddElementsForm, self).__init__(*args, **kwargs)
        if self.data.get('element_type', self.initial.get('element_type')) == 'p':
            protocols_to_add = user.get_protocols_to_add(
                selected_project)
            self.fields.get('element_choices').to_field_name = 'uuid'
            self.fields.get('element_choices').queryset = protocols_to_add
        elif self.data.get('element_type', self.initial.get('element_type')) == 's':
            sources_to_add = user.get_sources_to_add(selected_project)
            self.fields.get('element_choices').to_field_name = 'id'
            self.fields.get('element_choices').queryset = sources_to_add

    CHOICES = (
        ('p', 'Protocols'),
        ('s', 'Sources'))
    element_choices = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        to_field_name=None
    )
    element_type = forms.ChoiceField(CHOICES)

    def add_elements(self, selected_project):
        if self.cleaned_data:
            element_type = self.cleaned_data.get('element_type')
            if element_type == 'p':
                selected_project.protocols.add(*list(
                    self.cleaned_data.get('element_choices')))
            elif element_type == 's':
                selected_project.sources.add(*list(
                    self.cleaned_data.get('element_choices')))
