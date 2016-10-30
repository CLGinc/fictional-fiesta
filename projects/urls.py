from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^list/$', views.projects_list, name='projects_list'),
]
