from django.http import HttpResponseForbidden, HttpResponse
from django.http import HttpResponseBadRequest
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .forms import CreateInvitationModelForm
from .views import SingleInvitationMixin


@method_decorator(login_required, name='dispatch')
class CreateInvitation(View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            post = request.POST.copy()
            post['inviter'] = request.user.researcher.pk
            model_form = CreateInvitationModelForm(post or None)
            if model_form.is_valid():
                model_form.save()
                return HttpResponse('Invitation to {} created and sent!'.format(
                    model_form.cleaned_data['email'])
                )
            else:
                return HttpResponseBadRequest(
                    reason=model_form.errors.as_json()
                )
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
