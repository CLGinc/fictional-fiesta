from django.apps import AppConfig


class InvitationsConfig(AppConfig):
    name = 'invitations'

    def ready(self):
        import invitations.signals  # noqa
