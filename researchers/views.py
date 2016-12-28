from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout

from .forms import EmailAuthenticationForm, EmailUserCreationForm
from .models import Researcher


def login_user(request):
    next_redirect = request.GET.get('next')
    if request.user.is_authenticated():
        return redirect(reverse(settings.LOGIN_REDIRECT_URL))
    form = EmailAuthenticationForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user, user.backend)
                    if next_redirect:
                        return redirect(next_redirect)
                    else:
                        return redirect(reverse(settings.LOGIN_REDIRECT_URL))
    return render(request, 'login.html', locals())


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
