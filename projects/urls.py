from django.conf.urls import url

from . import views
from .ajax import GetProtocolsToAdd, GetSourcesToAdd
from .views import CreateProject

urlpatterns = [
    url(r'^list/$', views.projects_list, name='projects_list'),
    url(r'^create/$', CreateProject.as_view(), name='create_project'),
    url(r'^(?P<project_uid>[a-zA-Z0-9]{8})/$', views.project, name='project'),
    url(r'^(?P<project_uid>[a-zA-Z0-9]{8})/protocols_to_add/$', GetProtocolsToAdd.as_view(), name='project_get_protocols_to_add'),
    url(r'^(?P<project_uid>[a-zA-Z0-9]{8})/sources_to_add/$', GetSourcesToAdd.as_view(), name='project_get_sources_to_add'),
]
