from cerberus import Validator
from json import loads, decoder

from schemas.transactions_schema import transactions_schema
from services.transactions_service import create_transaction_service, get_transactions_service

transaction_validator = Validator(transactions_schema)


def create_transaction_controller(data: dict):
    if not isinstance(data, dict):
        return {'status': False, 'error': 'invalid request body'}, 400

    if not transaction_validator(data):
        return {'status': False, 'error': 'invalid request body'}, 400

    response = create_transaction_service(transaction=data)

    if response:
        return response, 201

    return {'status': False, 'error': '`code` invalid'}, 400


def get_transactions_controller(query_params: dict):
    page = query_params.get('page', 1)

    try:
        page = int(page)
    except ValueError:
        return {'status': False, 'error': 'invalid `page`'}, 400

    query_filter = query_params.get('filter', '{}')

    try:
        query_filter = loads(query_filter)
    except decoder.JSONDecodeError:
        return {'status': False, 'error': 'invalid `filter`'}, 400

    transactions = get_transactions_service(page=page, query_filter=query_filter)

    return transactions, 200
