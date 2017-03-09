from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .models import Role


ERROR_MESSAGE = _('Please enter a correct email and password. ')
ERROR_MESSAGE_RESTRICTED = _('You do not have permission to access the admin.')
ERROR_MESSAGE_INACTIVE = _('This account is inactive.')


class EmailAuthenticationForm(AuthenticationForm):
    '''
    Override the default AuthenticationForm to
     force email-as-username behavior.
    '''
    email = forms.EmailField(label=_('Email'), max_length=75)
    message_incorrect_password = ERROR_MESSAGE
    message_inactive = ERROR_MESSAGE_INACTIVE

    def __init__(self, request=None, *args, **kwargs):
        super(EmailAuthenticationForm, self).__init__(request, *args, **kwargs)
        del self.fields['username']
        self.fields.keyOrder = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if (self.user_cache is None):
                raise forms.ValidationError(self.message_incorrect_password)
            if not self.user_cache.is_active:
                raise forms.ValidationError(self.message_inactive)
        return self.cleaned_data


class EmailUserCreationForm(UserCreationForm):
    '''
    Override the default UserCreationForm to force email-as-username behavior.
    '''
    email = forms.EmailField(label=_('Email'), max_length=75)

    class Meta:
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(EmailUserCreationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError(
                _('A user with that email already exists.'))
        return email

    def save(self, commit=True):
        # Ensure that the username is set to the email address provided,
        # so the user_save_patch() will keep things in sync.
        self.instance.username = self.instance.email
        return super(EmailUserCreationForm, self).save(commit=commit)


class RoleListForm(forms.Form):
    ORDER_TYPE = (
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    )

    name = forms.CharField(max_length=255, required=False)
    created_from = forms.DateField(required=False)
    created_to = forms.DateField(required=False)
    role = forms.MultipleChoiceField(choices=Role.ROLES, required=False)
    order_by = forms.ChoiceField(required=False)
    order_type = forms.ChoiceField(choices=ORDER_TYPE, required=False)

    def __init__(self, *args, **kwargs):
        self.researcher = kwargs.pop('researcher')
        self.scope = kwargs.pop('scope')
        super(RoleListForm, self).__init__(*args, **kwargs)
        self.fields['order_by'].choices = self.get_order_by_choices()

    def get_order_by_choices(self):
        return (
            ('name', '{} Name'.format(str.capitalize(self.scope))),
            ('creation', 'Creation Date'),
            ('role', 'Role')
        )

    def is_valid(self):
        valid = super(RoleListForm, self).is_valid()
        if valid:
            self.cleaned_data = dict(
                (k, v) for k, v in self.cleaned_data.items() if v
            )
            self.generate_roles()
        return valid

    def get_order(self):
        order_replacement_model = {
            'name': '{}__name'.format(self.scope),
            'creation': '{}__datetime_created'.format(self.scope),
            'role': 'role',
            'asc': '',
            'desc': '-'
        }
        order_by = self.cleaned_data.get('order_by', 'creation')
        if order_by == 'creation':
            order_type = self.cleaned_data.get('order_type', 'desc')
        else:
            order_type = self.cleaned_data.get('order_type', 'asc')
        order_by = order_replacement_model[order_by]
        order_type = order_replacement_model[order_type]
        return order_type + order_by

    def generate_roles(self):
        """
        Generate roles based on form data.
        Query replacement model is used to replace form fields by their
        query counterpart. For example to filter by project name you need to
        add project__name__icontains to your filter.
        """
        field_replacement_model = {
            'name': '{}__name__icontains'.format(self.scope),
            'created_from': '{}__datetime_created__date__gte'.format(self.scope),
            'created_to': '{}__datetime_created__date__lte'.format(self.scope),
        }
        roles = self.researcher.get_roles(
            scope=self.scope,
            roles=self.cleaned_data.get('role', Role.get_db_roles()))
        data = dict()
        for key, value in field_replacement_model.items():
            if key in self.cleaned_data:
                data[value] = self.cleaned_data[key]
        roles = roles.filter(**data)
        # Order final list
        order_by = self.get_order()
        roles = roles.order_by(order_by)
        self.roles = roles
