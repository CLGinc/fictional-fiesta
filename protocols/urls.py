from django.conf.urls import url

from .views import ProtocoltList, ProtocolView, CreateProtocol, UpdateProtocol
from .views import CreateProtocolResult, ProtocolResultView
from .views import UpdateProtocolResult, ArchiveProtocol

uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

urlpatterns = [
    url(
        r'^list/$',
        ProtocoltList.as_view(),
        name='protocols_list'
    ),
    url(
        r'^create/$',
        CreateProtocol.as_view(),
        name='create_protocol'
    ),
    url(
        r'^(?P<protocol_uuid>{})/update/$'.format(uuid_pattern),
        UpdateProtocol.as_view(),
        name='update_protocol'
    ),
    url(
        r'^(?P<protocol_uuid>{})/archive/$'.format(uuid_pattern),
        ArchiveProtocol.as_view(),
        name='archive_protocol'
    ),
    url(
        r'^(?P<protocol_uuid>{})/$'.format(uuid_pattern),
        ProtocolView.as_view(),
        name='protocol'
    ),
    url(
        r'^(?P<protocol_uuid>{})/result/create/$'.format(uuid_pattern),
        CreateProtocolResult.as_view(),
        name='create_protocol_result'
    ),
    url(
        r'^(?P<protocol_uuid>{})/result/(?P<result_uuid>{})/$'.format(uuid_pattern, uuid_pattern),
        ProtocolResultView.as_view(),
        name='protocol_result'
    ),
    url(
        r'^(?P<protocol_uuid>{})/result/(?P<result_uuid>{})/update/$'.format(uuid_pattern, uuid_pattern),
        UpdateProtocolResult.as_view(),
        name='update_protocol_result'
    ),
]
