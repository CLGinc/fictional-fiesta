from django.conf.urls import url

from .views import ProtocoltList, ProtocolView, CreateProtocol, EditProtocol

urlpatterns = [
    url(r'^list/$', ProtocoltList.as_view(), name='protocols_list'),
    url(r'^create/$', CreateProtocol.as_view(), name='create_protocol'),
    url(r'^(?P<protocol_uid>[a-zA-Z0-9]{8})/edit/$', EditProtocol.as_view(), name='edit_protocol'),
    url(r'^(?P<protocol_uid>[a-zA-Z0-9]{8})/$', ProtocolView.as_view(), name='protocol'),
]
