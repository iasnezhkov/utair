import click
from flask.cli import AppGroup
from flask.cli import with_appcontext
from json import load
from flask import current_app
from os.path import join
from random import randint, choice
from utils import generate_code
from datetime import datetime
import requests
from werkzeug.security import generate_password_hash

from extensions import mongo

populate_cli = AppGroup('populate')


@populate_cli.command('populate_users')
@with_appcontext
def populate_users_command():
    app_root_folder = current_app.config.get('APP_ROOT_FOLDER')
    sample_path = join(app_root_folder, 'management/users.json')

    with open(sample_path) as users:
        users = load(users)

        for user in users:
            user['password'] = generate_password_hash(user.get('password'))
            res = mongo.db.users.update({'email': user.get('email')}, {'$set': user}, True)
            click.echo('{email} updated existing: {updated}'.format(email=user.get('email'),
                                                                    updated=res.get('updatedExisting', False)))


def get_transaction(card_number: int, date_format: str):
    transaction = {
        "user_card_number": card_number,
        "bonus_miles": randint(300, 3000),
        "departure_location": generate_code(),
        "arrival_location": generate_code(),
        "departure_date": datetime.utcfromtimestamp(randint(1446372000, 1535365267)).strftime(date_format),
    }

    return transaction


def get_auth_token(host: str, credentials: dict):
    url = '{host}/api/v1/auth/sign-in'.format(host=host)
    response = requests.post(url, json=credentials)
    response_json = response.json()
    access_token = response_json.get('access_token')

    return access_token


@populate_cli.command('populate_transactions')
@click.option('--host', default='http://127.0.0.1:5000')
@click.option('--count', default=100)
@with_appcontext
def populate_transactions_command(host: str, count: int):
    date_format = current_app.config.get('DATE_FORMAT')
    app_root_folder = current_app.config.get('APP_ROOT_FOLDER')
    sample_path = join(app_root_folder, 'management/users.json')

    with open(sample_path) as users:
        credentials = {
            "email": "service@test.test",
            "password": "service",
        }
        access_token = get_auth_token(host=host, credentials=credentials)
        users = load(users)
        user_card_numbers = [user.get('card_number') for user in users]

        for i in range(count):
            url = '{host}/api/v1/transactions'.format(host=host)
            headers = {
                'Authorization': 'Bearer {access_token}'.format(access_token=access_token)
            }
            transaction = get_transaction(card_number=choice(user_card_numbers), date_format=date_format)
            response = requests.post(url=url, headers=headers, json=transaction)
            click.echo(response.json())
