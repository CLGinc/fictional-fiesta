from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^create/$', ajax.create_invitation, name='create_invitation'),
    url(r'^accept/$', ajax.accept_invitation, name='accept_invitation'),
    url(r'^list/$', views.InvitationsList.as_view(), name='invitations_list'),
    url(r'^assign/(?P<slug>[a-zA-Z0-9]{64})/$', views.AssignInvitation.as_view(), name='assign_invitation'),
]
