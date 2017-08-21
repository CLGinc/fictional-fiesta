from django.conf.urls import url

from .ajax import AddProtocols, AddSources, ArchiveProject
from .views import CreateProject, ProjectList, ProjectView, UpdateProject

uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(
        r'^list/$',
        ProjectList.as_view(),
        name='projects_list'
    ),
    url(
        r'^create/$',
        CreateProject.as_view(),
        name='create_project'
    ),
    url(
        r'^(?P<project_uuid>{})/update/$'.format(uuid_pattern),
        UpdateProject.as_view(),
        name='update_project'
    ),
    url(
        r'^(?P<project_uuid>{})/archive/$'.format(uuid_pattern),
        ArchiveProject.as_view(),
        name='archive_project'
    ),
    url(
        r'^(?P<project_uuid>{})/$'.format(uuid_pattern),
        ProjectView.as_view(),
        name='project'
    ),
    url(
        r'^(?P<project_uuid>{})/add_protocols/$'.format(uuid_pattern),
        AddProtocols.as_view(),
        name='add_protocols_to_project'
    ),
    url(
        r'^(?P<project_uuid>{})/add_sources/$'.format(uuid_pattern),
        AddSources.as_view(),
        name='project_add_sources'
    ),
]
