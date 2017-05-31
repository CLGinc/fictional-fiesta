from django.conf.urls import url

from .views import Login, Logout, Register

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login_user'),
    url(r'^logout/$', Logout.as_view(), name='logout_user'),
    url(r'^register/$', Register.as_view(), name='register_user'),
]
