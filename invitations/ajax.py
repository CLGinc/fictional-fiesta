from django.http import HttpResponseForbidden, HttpResponse
from django.http import HttpResponseBadRequest


from .forms import CreateInvitationForm


def create_invitation(request):
    if request.is_ajax() and request.method == 'POST':
        form = CreateInvitationForm(request.POST or None)
        if form.is_valid():
            invitation = form.save()
            invitation.send()
        else:
            return HttpResponseBadRequest(reason=form.errors)
    else:
        return HttpResponseForbidden()
