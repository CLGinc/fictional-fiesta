from django.conf.urls import url

from . import views, ajax

urlpatterns = [
    url(r'^list/$', views.projects_list, name='projects_list'),
    url(r'^(?P<unique_id>\w+)/$', views.project, name='project'),
    url(r'^(?P<project_uid>\w+)/protocols_to_add/$', ajax.get_protocols_to_add, name='project_get_protocols_to_add'),
]
