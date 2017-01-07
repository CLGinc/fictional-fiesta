from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.projects_list, name='projects_list'),
    url(r'^(?P<project_uid>\w+)/$', views.project, name='project'),
]
