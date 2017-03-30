from django.conf.urls import url

from .ajax import AddProtocols, AddSources
from .views import CreateProject, ProjectList, ProjectView

urlpatterns = [
    url(r'^list/$', ProjectList.as_view(), name='projects_list'),
    url(r'^create/$', CreateProject.as_view(), name='create_project'),
    url(r'^edit/$', CreateProject.as_view(), name='edit_project'),
    url(r'^(?P<project_uid>[a-zA-Z0-9]{8})/$', ProjectView.as_view(), name='project'),
    url(r'^(?P<project_uid>[a-zA-Z0-9]{8})/add_protocols/$', AddProtocols.as_view(), name='project_add_protocols'),
    url(r'^(?P<project_uid>[a-zA-Z0-9]{8})/add_sources/$', AddSources.as_view(), name='project_add_sources'),
]
