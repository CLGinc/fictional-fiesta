from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView

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


def logout_user(request):
    logout(request)
    return redirect(reverse(settings.LOGOUT_REDIRECT_URL))


def register_user(request):
    next_redirect = request.GET.get('next')
    if request.user.is_authenticated():
        return redirect(reverse(settings.REGISTER_REDIRECT_URL))
    form = EmailUserCreationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            user = form.instance
            Researcher.objects.create(user=user)
            login(request, user, 'django.contrib.auth.backends.ModelBackend')
            if next_redirect:
                return redirect(next_redirect)
            else:
                return redirect(reverse(settings.REGISTER_REDIRECT_URL))
    return render(request, 'register.html', locals())
