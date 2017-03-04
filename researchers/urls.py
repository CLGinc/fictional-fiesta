from django.conf.urls import url

from .views import LoginView, LogoutView, register_user

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login_user'),
    url(r'^logout/$', LogoutView.as_view(), name='logout_user'),
    url(r'^register/$', register_user, name='register_user'),
]
