from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login, logout

from .forms import EmailAuthenticationForm


def login_user(request):
    if request.user.is_authenticated():
        return redirect(reverse(settings.LOGIN_REDIRECT_URL))
    form = EmailAuthenticationForm(None, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse(settings.LOGIN_REDIRECT_URL))
    return render(request, 'login.html', locals())


def logout_user(request):
    logout(request)
    return redirect(reverse(settings.LOGOUT_REDIRECT_URL))
