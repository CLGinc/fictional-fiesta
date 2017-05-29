from django.apps import AppConfig


class ProtocolsConfig(AppConfig):
    name = 'protocols'

    def ready(self):
        import protocols.signals  # noqa
