from django.http import HttpResponseForbidden, HttpResponse
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404


from .forms import CreateInvitationForm, CreateInvitationModelForm
from .models import Invitation
from .views import SingleInvitationMixin


@method_decorator(login_required, name='dispatch')
class CreateInvitation(View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
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
        return HttpResponseForbidden()

@method_decorator(login_required, name='dispatch')
class AcceptInvitation(SingleInvitationMixin, View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            self.object = self.get_object()
            if self.object.can_be_accepted(self.request.user.researcher):
                self.object.accept(invited=self.request.user.researcher)
                return HttpResponse('Invitation accepted!')
        return HttpResponseForbidden()
