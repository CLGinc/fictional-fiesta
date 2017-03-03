from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

from .models import Invitation


class InvitationsList(ListView):
    context_object_name = 'invitations_list'
    template_name = 'invitations_list.html'

    def get_queryset(self):
        return Invitation.objects.filter(invited=self.request.user.researcher)
