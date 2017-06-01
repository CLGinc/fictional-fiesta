from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from django.views.generic.base import RedirectView
from django.contrib.auth.views import LogoutView, LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import MultipleObjectMixin

from .forms import EmailAuthenticationForm, EmailUserCreationForm, RoleListForm


class Login(LoginView):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'login.html'
    authentication_form = EmailAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(Login, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get(
            'next',
            reverse(self.success_url)
        )

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['next_redirect'] = self.get_success_url()
        return context


class Register(CreateView):
    success_url = settings.REGISTER_REDIRECT_URL
    template_name = 'register.html'
    form_class = EmailUserCreationForm

    def get_success_url(self):
        return self.request.GET.get(
            'next',
            reverse(self.success_url)
        )

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(Register, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['next_redirect'] = self.get_success_url()
        return context


@method_decorator(login_required, name='dispatch')
class Logout(LogoutView):
    next_page = settings.LOGOUT_REDIRECT_URL


class RoleListMixin(MultipleObjectMixin):
    paginate_by = 15

    def get_queryset(self):
        roles_list = None
        self.form = RoleListForm(
            self.request.GET,
            user=self.request.user,
            scope=self.scope
        )
        if self.form.is_valid():
            roles_list = self.form.roles
        return roles_list

    def get_context_data(self, **kwargs):
        context = super(RoleListMixin, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context


@method_decorator(login_required, name='dispatch')
class HomePage(RedirectView):
    pattern_name = 'projects_list'
