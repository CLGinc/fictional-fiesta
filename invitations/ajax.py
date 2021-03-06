from django.http import HttpResponseForbidden, JsonResponse
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .models import Invitation
from .views import SingleInvitationMixin


@method_decorator(login_required, name='dispatch')
class CreateInvitation(CreateView):
    model = Invitation
    fields = [
        'email',
        'inviter',
        'invited',
        'protocol',
        'project',
        'role',
    ]
    http_method_names = ['post']

    def form_invalid(self, form):
        super(CreateInvitation, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return HttpResponseForbidden()

    def form_valid(self, form):
        super(CreateInvitation, self).form_valid(form)
        if self.request.is_ajax():
            invited_name = None
            if self.object.invited:
                invited_name = self.object.invited.get_full_name()
            data = {
                'pk': self.object.pk,
                'invited_email': self.object.email,
                'invited_name': invited_name
            }
            return JsonResponse(data, status=201)
        else:
            return HttpResponseForbidden()

    def get_form_kwargs(self):
        kwargs = super(CreateInvitation, self).get_form_kwargs()
        if 'data' in kwargs:
            kwargs['data'] = kwargs['data'].copy()
            kwargs['data']['inviter'] = str(self.request.user.pk)
        return kwargs

    def get_success_url(self):
        return reverse('invitations:invitations_list')


@method_decorator(login_required, name='dispatch')
class AcceptInvitation(SingleInvitationMixin, View):
    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            self.object = self.get_object()
            if self.object.can_be_accepted(self.request.user):
                self.object.accept()
                data = {
                    'pk': self.object.pk,
                    'accepted': self.object.accepted
                }
                return JsonResponse(data, status=200)
        return HttpResponseForbidden()
