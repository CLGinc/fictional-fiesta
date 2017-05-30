from jsonschema import validate
import jsonschema


def vaidate_result_data_columns(value, data_type):
    data_columns_schema = {
        'type': 'object',
        'properties': {
            'data_columns': {
                'type': 'array',
                'minItems': 2,
                'maxItems': 50,
                'items': {
                    '$ref': '#/definitions/data_column'
                }
            }
        },
        'required': ['data_columns', ],
        'definitions': {
            'data_column': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 50,
                        'items': {
                            'type': data_type
                        }
                    },
                    'title': {
                        'type': 'string',
                        'maxLength': 255,
                    },
                    'variable': {
                        'type': 'string',
                        'enum': [
                            'dependent',
                            'independent'
                        ]
                    }
                },
                'required': ['data', 'title', 'variable'],
            }
        }
    }
    error_message = None
    try:
        validate(value, data_columns_schema)
        for idx, column in enumerate(value['data_columns']):
            if (idx == 0 and column['variable'] != 'independent') or \
                    (idx != 0 and column['variable'] == 'independent'):
                error_message = '"variable" must be "independent" only in the first column and "dependent" in the rest!'
    except jsonschema.exceptions.ValidationError as e:
        error_message = e.message
    return error_message


def vaidate_protocol_procedure(value):
    procedure_schema = {
        'type': 'object',
        'properties': {
            'steps': {
                'type': 'array',
                'minItems': 1,
                'maxItems': 50,
                'items': {
                    '$ref': '#/definitions/step'
                }
            }
        },
        'required': ['steps', ],
        'definitions': {
            'step': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'string',
                        'maxLength': 255,
                    },
                    'description': {
                        'type': 'string',
                        'maxLength': 255,
                    }
                },
                'required': ['title', 'description'],
            }
        }
    }
    error_message = None
    try:
        validate(value, procedure_schema)
    except jsonschema.exceptions.ValidationError as e:
        error_message = e.message
    return error_message
