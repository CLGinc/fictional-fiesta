from .models import Researcher


def create_researcher(backend, user, response, *args, **kwargs):
    if not(Researcher.objects.filter(user=user).exists()):
        Researcher.objects.create(user=user)
