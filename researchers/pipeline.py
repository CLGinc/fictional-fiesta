from .models import Researcher


def create_researcher(backend, user, response, *args, **kwargs):
    Researcher.objects.get_or_create(user=user)
