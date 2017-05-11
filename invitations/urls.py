from django.conf.urls import url

from .views import InvitationsList, AssignInvitation
from .ajax import CreateInvitation, AcceptInvitation

uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(r'^create/$', CreateInvitation.as_view(), name='create_invitation'),
    url(r'^(?P<uuid>{})/accept/$'.format(uuid_pattern), AcceptInvitation.as_view(), name='accept_invitation'),
    url(r'^list/$', InvitationsList.as_view(), name='invitations_list'),
    url(r'^(?P<uuid>{})/assign/$'.format(uuid_pattern), AssignInvitation.as_view(), name='assign_invitation'),
]
