from django.conf.urls import url

from .views import ProtocoltList

urlpatterns = [
    url(r'^list/$', ProtocoltList.as_view(), name='protocols_list'),
]
