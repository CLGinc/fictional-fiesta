from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

from .models import Invitation


@login_required
def accept_invitation(request):
    key = request.GET.get('key') or request.POST.get('key')
    invitation = get_object_or_404(Invitation, key=key)
    if invitation.can_be_accepted(request.user.researcher):
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
        return render(request, 'accept_invitation.html', locals())
    return HttpResponseForbidden()
