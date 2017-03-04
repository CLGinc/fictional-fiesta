from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView

from .forms import EmailAuthenticationForm, EmailUserCreationForm
from .models import Researcher


class LoginView(FormView):
    template_name = 'login.html'
    form_class = EmailAuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        if user is not None:
            if user.is_active:
                login(self.request, user, user.backend)
        return super(LoginView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['next_redirect'] = self.get_success_url()
        return context

    def get_success_url(self):
        return self.request.GET.get(
            'next',
            reverse(settings.LOGIN_REDIRECT_URL)
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse(settings.LOGIN_REDIRECT_URL))
        return super(LoginView, self).get(request, *args, **kwargs)


class LogoutView(RedirectView):
    pattern_name = settings.LOGOUT_REDIRECT_URL

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = EmailUserCreationForm

    def form_valid(self, form):
        form.save()
        user = form.instance
        Researcher.objects.create(user=user)
        login(self.request, user, 'django.contrib.auth.backends.ModelBackend')
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        context['next_redirect'] = self.get_success_url()
        return context

    def get_success_url(self):
        return self.request.GET.get(
            'next',
            reverse(settings.REGISTER_REDIRECT_URL)
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse(settings.REGISTER_REDIRECT_URL))
        return super(RegisterView, self).get(request, *args, **kwargs)
