from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Invitation


def accept_invitation(request, key):
    try:
        invitation = Invitation.objects.get(key=key)
    except Invitation.DoesNotExist:
        raise Http404()
    if request.method == 'GET':
        if request.user.is_authenticated():
            pass
        else:
            return redirect(reverse(settings.LOGIN_URL)+'?next={}'.format(invitation.key))
