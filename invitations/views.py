from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .models import Invitation
from .forms import AcceptInvitationForm


@login_required
def accept_invitation(request):
    key = request.GET.get('key') or request.POST.get('key')
    invitation = get_object_or_404(Invitation, key=key)
    if invitation.is_expired() or \
            invitation.inviter == request.user.researcher or \
            invitation.accepted or \
            invitation.invited:
        raise Http404()
    form = AcceptInvitationForm({'key': key})
    if request.method == 'POST':
        if form.is_valid():
            invitation.accept(invited=request.user.researcher)
            if invitation.project:
                return redirect(
                    reverse(
                        'project',
                        args=[invitation.project.id]
                    )
                )
            elif invitation.protocol:
                return redirect(
                    reverse(
                        'protocol',
                        args=[invitation.protocol.id]
                    )
                )
    return render(request, 'accept_invitation.html', locals())
