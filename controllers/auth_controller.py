import re

from schemas.users_schema import email_regex
from services.auth_service import request_code_service, code_sign_in_service, sign_in_service


def request_code_controller(data: dict):
    if not isinstance(data, dict):
        return {'status': False, 'error': 'invalid request body'}, 400

    email = data.get('email')

    if not email:
        return {'status': False, 'error': '`email` is required'}, 400

    if not re.match(email_regex, email):
        return {'status': False, 'error': '`email` is invalid'}, 400

    response = request_code_service(email=email)

    if response:
        return response, 200

    return {'status': False, 'error': 'email not sent or user not exists'}, 400


def code_sign_in_controller(data: dict):
    if not isinstance(data, dict):
        return {'status': False, 'error': 'invalid request body'}, 400

    code = data.get('code')

    if not code:
        return {'status': False, 'error': '`code` is required'}, 400

    response = code_sign_in_service(code=code)

    if response:
        return response, 200

    return {'status': False, 'error': '`code` invalid'}, 400


def sign_in_controller(data: dict):
    if not isinstance(data, dict):
        return {'status': False, 'error': 'invalid request body'}, 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return {'status': False, 'error': '`email` and `password` is required'}, 400

    if not re.match(email_regex, email):
        return {'status': False, 'error': '`email` is invalid'}, 400

    tokens = sign_in_service(email=email, password=password)

    if not tokens:
        return {'sign-in': False}, 400

    return tokens, 200
