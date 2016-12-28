from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Invitation
from .forms import AcceptInvitationForm


def accept_invitation(request):
    key = request.GET.get('key') or request.POST.get('key')
    invitation = get_object_or_404(Invitation, key=key)
    next_redirect = '?next={}?key={}'.format(reverse('accept_invitation'), key)
    form = AcceptInvitationForm({'key': key})
    if request.method == 'POST':
        if form.is_valid():
            invitation.accept(invited=request.user.researcher)
            if invitation.project:
                return redirect(
                    reverse(
                        'project',
                        args=[invitation.project.unique_id]
                    )
                )
            elif invitation.protocol:
                return redirect(
                    reverse(
                        'protocol',
                        args=[invitation.protocol.unique_id]
                    )
                )
    if request.user.is_authenticated():
        return render(request, 'accept_invitation.html', locals())
    else:
        return redirect(reverse(settings.LOGIN_URL)+next_redirect)
