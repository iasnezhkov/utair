from bson import ObjectId
from flask_jwt_extended import get_jwt_identity

from extensions import mongo
from flask import current_app
from datetime import datetime
from random import randint


def create_transaction_service(transaction: dict):
    date_format = current_app.config.get('DATE_FORMAT')
    transaction['transaction_number'] = randint(10000000000000000, 99999999999999999)
    transaction['departure_date'] = datetime.strptime(transaction.get('departure_date'), date_format)
    transaction_id = mongo.db.transactions.insert(transaction)

    if transaction_id:
        transaction['_id'] = str(transaction.get('_id'))
        return transaction

    return False


def get_transactions_service(query_filter: dict, page: int = 1):
    limit = 25
    skip = limit * (page - 1)

    current_user = get_jwt_identity()

    if not current_user:
        return None

    user = mongo.db.users.find_one({'_id': ObjectId(current_user)}, {'_id': False, 'password': False})

    if not user:
        return None

    query_filter['user_card_number'] = user.get('card_number')

    transactions = mongo.db.transactions.find(query_filter, {'_id': False}).skip(skip).limit(limit)
    transactions = list(transactions)

    return transactions
