transactions_schema = {
    'transaction_number': {
        'type': 'number',
    },
    'user_card_number': {
        'type': 'number',
        'required': True,
    },
    'bonus_miles': {
        'type': 'number',
        'required': True,
    },
    'departure_location': {
        'type': 'string',
        'required': True,
    },
    'arrival_location': {
        'type': 'string',
        'required': True,
    },
    'departure_date': {
        'type': 'string',
        'regex': '\w+, \d+ \w+ \d+ \d+:\d+:\d+ GMT',
        'required': True,
    },
}
