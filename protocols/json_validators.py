from jsonschema import validate
import jsonschema


def vaidate_result_data_columns(
        value,
        data_type_independent,
        data_type_dependent):
    data_columns_schema = {
        'type': 'object',
        'properties': {
            'independent_variable': {
                'type': 'array',
                'minItems': 1,
                'maxItems': 1,
                'items': {
                    '$ref': '#/definitions/data_column_independent'
                }
            },
            'dependent_variable': {
                'type': 'array',
                'minItems': 1,
                'maxItems': 50,
                'items': {
                    '$ref': '#/definitions/data_column_dependent'
                }
            }
        },
        'required': ['independent_variable', 'dependent_variable'],
        'definitions': {
            'data_column_independent': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 50,
                        'items': {
                            'type': data_type_independent
                        }
                    },
                    'title': {
                        'type': 'string',
                        'maxLength': 255,
                    }
                },
                'required': ['data', 'title'],
            },
            'data_column_dependent': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 50,
                        'items': {
                            'type': data_type_dependent
                        }
                    },
                    'title': {
                        'type': 'string',
                        'maxLength': 255,
                    }
                },
                'required': ['data', 'title'],
            }
        }
    }
    error_message = None
    try:
        validate(value, data_columns_schema)
        column_size = len(
            value['independent_variable'][0]['data']
        )
        for column in value['dependent_variable']:
            if column_size != len(column['data']):
                error_message = 'All columns must have the same number of rows!'
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
                        'maxLength': 1024,
                        'minLength': 1,
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
