from django.conf.urls import url

from . import views
from .views import LoginView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^register/$', views.register_user, name='register_user'),
]
