from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin

from .models import Invitation


class SingleInvitationMixin(SingleObjectMixin):
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_queryset(self):
        return Invitation.objects.filter(
            email=self.request.user.email
        )


@method_decorator(login_required, name='dispatch')
class InvitationsList(ListView):
    context_object_name = 'invitations_list'
    template_name = 'invitations_list.html'

    def get_queryset(self):
        return Invitation.objects.filter(invited=self.request.user)
