email_regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

users_schema = {
    'full_name': {
        'type': 'string',
        'required': True,
    },
    'email': {
        'type': 'string',
        'regex': email_regex,
        'required': True,
    },
    'password': {
        'type': 'string',
    },
    'card_number': {
        'type': 'number',
    },
    'roles': {
        'type': 'list',
        'schema': {
            'type': 'string',
            'allowed': ['user', 'service'],
        }
    },
}
