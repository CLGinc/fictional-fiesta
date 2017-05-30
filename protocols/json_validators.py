from jsonschema import validate
import jsonschema

from django.core.exceptions import ValidationError


def vaidate_result_data_columns(value, data_type, field_name):
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
    try:
        validate(value, data_columns_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(
            {field_name: 'The input JSON is not valid: {}!'.format(e.message)}
        )
    return True


def vaidate_protocol_procedure(value, field_name):
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
    try:
        validate(value, procedure_schema)
    except jsonschema.exceptions.ValidationError as e:
        raise ValidationError(
            {field_name: 'The input JSON is not valid: {}!'.format(e.message)}
        )
    return True
