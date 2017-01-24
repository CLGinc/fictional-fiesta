from SciLog.utils import generate_string_for_model


def generate_uid():
    return generate_string_for_model(
        8,
        'protocols',
        'Protocol',
        'unique_id')
