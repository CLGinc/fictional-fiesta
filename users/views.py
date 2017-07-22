from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, TemplateView, DetailView
from django.views.generic.base import RedirectView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import LogoutView, LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.list import MultipleObjectMixin
from django.http import Http404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import login


from .forms import EmailAuthenticationForm, EmailUserCreationForm, RoleListForm
from .models import User


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

    def form_valid(self, form):
        form.instance.is_active = False
        self.object = form.save()
        token = default_token_generator.make_token(self.object)
        username_base64 = urlsafe_base64_encode(
            force_bytes(self.object.username)
        )
        self.template_name = 'register_success.html'
        url = reverse(
            'users:activate_user',
            kwargs={'username': username_base64, 'token': token}
        )
        variables = {
            'user': str(self.object),
            'url': url
        }
        self.object.email_user(
            template_id=settings.MJ_EMAIL_CONFIRMATION_TEMPLATE_ID,
            variables=variables,
            from_email=settings.MJ_EMAIL_CONFIRMATION_FROM,
            fail_silently=settings.DEBUG
        )
        return self.render_to_response(self.get_context_data())

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(Register, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['next_redirect'] = self.get_success_url()
        return context


class ActivateUser(RedirectView):
    pattern_name = 'home_page'

    def get(self, request, *args, **kwargs):
        username_base64 = kwargs.pop('username')
        token = kwargs.pop('token')
        if not request.user.is_authenticated():
            try:
                username = urlsafe_base64_decode(username_base64)
                user = User.objects.get(username=username)
                if default_token_generator.check_token(user, token) and \
                        user.is_active is False:
                    user.is_active = True
                    user.save()
                    login(request, user, 'django.contrib.auth.backends.ModelBackend')
                    return super(ActivateUser, self).get(request, *args, **kwargs)
            except:
                pass
        raise Http404


@method_decorator(login_required, name='dispatch')
class Logout(LogoutView):
    next_page = 'users:login_user'


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
class HomePage(TemplateView):
    template_name = 'home_page.html'

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['number_of_projects'] = self.request.user.get_roles(
            scope='project'
        ).count()
        context['number_of_protocols'] = self.request.user.get_roles(
            scope='protocol'
        ).count()
        invitations = [i for i in self.request.user.get_invitations(accepted=False) if i.is_expired() is False]
        context['number_of_invitations'] = len(invitations)
        return context


@method_decorator(login_required, name='dispatch')
class ProfilePage(DetailView):
    context_object_name = 'auth_user'
    template_name = 'profile_page.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
        social_auths = self.request.user.social_auth.all()
        for social_auth in social_auths:
            context[social_auth.provider.replace('-', '_')] = social_auth
        return context


@method_decorator(login_required, name='dispatch')
class UpdateProfile(UpdateView):
    context_object_name = 'auth_user'
    template_name = 'update_profile_page.html'
    fields = ['first_name', 'last_name', 'scientific_degree']

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:profile_page')
