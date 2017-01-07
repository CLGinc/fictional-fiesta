from SciLog.utils import generate_string_for_model


def generate_key():
    return generate_string_for_model(
        64,
        'invitations',
        'Invitation',
        'key')
