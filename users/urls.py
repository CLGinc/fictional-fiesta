from django.conf.urls import url

from .views import Login, Logout, Register, HomePage, ActivateUser

urlpatterns = [
    url(r'^login/$', Login.as_view(), name='login_user'),
    url(r'^logout/$', Logout.as_view(), name='logout_user'),
    url(r'^register/$', Register.as_view(), name='register_user'),
    url(r'^activate/(?P<username>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', ActivateUser.as_view(), name='activate_user'),
    url(r'^$', HomePage.as_view(), name='home_page'),
]
