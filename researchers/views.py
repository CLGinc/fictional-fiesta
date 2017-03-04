from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .forms import EmailAuthenticationForm, EmailUserCreationForm
from .models import Researcher


class BaseAuthView(FormView):
    redirect_url = ''

    def get_context_data(self, **kwargs):
        context = super(BaseAuthView, self).get_context_data(**kwargs)
        context['next_redirect'] = self.get_success_url()
        return context

    def get_success_url(self):
        return self.request.GET.get(
            'next',
            reverse(self.redirect_url)
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.redirect_url)
        return super(BaseAuthView, self).get(request, *args, **kwargs)


class Login(BaseAuthView):
    redirect_url = settings.LOGIN_REDIRECT_URL
    template_name = 'login.html'
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            if user.is_active:
                login(self.request, user, user.backend)
        return super(Login, self).form_valid(form)


class Register(BaseAuthView):
    redirect_url = settings.REGISTER_REDIRECT_URL
    template_name = 'register.html'
    form_class = EmailUserCreationForm

    def form_valid(self, form):
        form.save()
        user = form.instance
        Researcher.objects.create(user=user)
        login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return super(Register, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class Logout(RedirectView):
    pattern_name = settings.LOGOUT_REDIRECT_URL

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(Logout, self).get_redirect_url(*args, **kwargs)
