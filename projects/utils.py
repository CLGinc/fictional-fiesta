from SciLog.utils import generate_string_for_model


def generate_uid():
    return generate_string_for_model(
        8,
        'projects',
        'Project',
        'unique_id')
