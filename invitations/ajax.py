from django.http import HttpResponseForbidden, HttpResponse
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


from .forms import CreateInvitationForm, CreateInvitationModelForm
from .models import Invitation


@login_required
def create_invitation(request):
    if request.is_ajax() and request.method == 'POST':
        form = CreateInvitationForm(
            request.POST or None,
            inviter=request.user.researcher
        )
        if form.is_valid():
            model_form = CreateInvitationModelForm(
                form.get_data_for_model_form(request.user.researcher)
            )
            if model_form.is_valid():
                model_form.save()
                return HttpResponse('Invitation to {} created \
and sent!'.format(model_form.cleaned_data['email'])
                )
            else:
                return HttpResponseBadRequest(
                    reason=model_form.errors.as_json()
                )
        else:
                return HttpResponseBadRequest(reason=form.errors.as_json())
    else:
        return HttpResponseForbidden()

@login_required
def accept_invitation(request):
    if request.is_ajax() and request.method == 'POST':
        key = request.POST.get('key')
        invitation = get_object_or_404(Invitation, key=key)
        if invitation.can_be_accepted(request.user.researcher):
            invitation.accept(invited=request.user.researcher)
            return HttpResponse('Invitation accepted!')
    return HttpResponseForbidden()
