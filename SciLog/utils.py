from django.utils.crypto import get_random_string
from django.apps import apps


def generate_string_for_model(length, app_label, model_name, field_name):
    Model = apps.get_model(app_label, model_name)
    while(True):
        value = get_random_string(length)
        data = {field_name: value}
        try:
            Model.objects.get(**data)
        except Model.DoesNotExist:
            return value
