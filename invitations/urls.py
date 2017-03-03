from django.conf.urls import url

from .views import InvitationsList, AssignInvitation
from .ajax import create_invitation, AssignInvitation

urlpatterns = [
    url(r'^create/$', create_invitation, name='create_invitation'),
    url(r'^(?P<key>[a-zA-Z0-9]{64})/accept/$', AssignInvitation.as_view(), name='accept_invitation'),
    url(r'^list/$', InvitationsList.as_view(), name='invitations_list'),
    url(r'^(?P<key>[a-zA-Z0-9]{64})/assign/$', AssignInvitation.as_view(), name='assign_invitation'),
]
