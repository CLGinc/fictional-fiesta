from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from .models import Invitation


@method_decorator(login_required, name='dispatch')
class InvitationsList(ListView):
    context_object_name = 'invitations_list'
    template_name = 'invitations_list.html'

    def get_queryset(self):
        return Invitation.objects.filter(invited=self.request.user.researcher)

class SingleInvitationMixin(SingleObjectMixin):
    slug_field = 'key'

    def get_queryset(self):
        return Invitation.objects.filter(
            email=self.request.user.email
        )

@method_decorator(login_required, name='dispatch')
class AssignInvitation(SingleInvitationMixin, View):
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not(self.object.invited):
            self.object.invited = self.request.user.researcher
            self.object.save()
        return redirect(reverse('invitations_list'))
