from django.conf.urls import url

from .views import ProtocoltList, ProtocolView

urlpatterns = [
    url(r'^list/$', ProtocoltList.as_view(), name='protocols_list'),
    url(r'^(?P<protocol_uid>[a-zA-Z0-9]{8})/$', ProtocolView.as_view(), name='project'),
]
