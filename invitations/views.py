from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Invitation


def accept_invitation(request, key):
    invitation = get_object_or_404(Invitation, key=key)
    next_redirect = '?next={}'.format(reverse('accept_invitation', args=[key]))
    print(next_redirect)
    if request.method == 'GET':
        if request.user.is_authenticated():
            return render(request, 'accept_invitation.html', locals())
        else:
            return redirect(reverse(settings.LOGIN_URL)+next_redirect)
