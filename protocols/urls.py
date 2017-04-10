from django.conf.urls import url

from .views import ProtocoltList, ProtocolView, CreateProtocol, UpdateProtocol

urlpatterns = [
    url(r'^list/$', ProtocoltList.as_view(), name='protocols_list'),
    url(r'^create/$', CreateProtocol.as_view(), name='create_protocol'),
    url(r'^(?P<protocol_uid>[a-zA-Z0-9]{8})/update/$', UpdateProtocol.as_view(), name='update_protocol'),
    url(r'^(?P<protocol_uid>[a-zA-Z0-9]{8})/$', ProtocolView.as_view(), name='protocol'),
]
