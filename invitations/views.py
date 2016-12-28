from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Invitation


def accept_invitation(request, key):
    invitation = get_object_or_404(Invitation, key=key)
    if request.method == 'GET':
        if request.user.is_authenticated():
            pass
        else:
            return redirect(reverse(settings.LOGIN_URL)+'?next={}'.format(invitation.key))
