from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _


ERROR_MESSAGE = _("Please enter a correct email and password. ")
ERROR_MESSAGE_RESTRICTED = _("You do not have permission to access the admin.")
ERROR_MESSAGE_INACTIVE = _("This account is inactive.")


class EmailAuthenticationForm(AuthenticationForm):
    """
    Override the default AuthenticationForm to
     force email-as-username behavior.
    """
    email = forms.EmailField(label=_("Email"), max_length=75)
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
