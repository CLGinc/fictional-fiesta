from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^create/$', ajax.create_invitation, name='create_invitation'),
]
