from bson import ObjectId
from flask import current_app, session, abort
from threading import Thread
from functools import wraps
from flask_jwt_extended import create_access_token, create_refresh_token, get_jti, get_raw_jwt, get_jwt_identity
from werkzeug.security import check_password_hash

from extensions import mongo, cache, jwt
from utils import send_email, generate_code


def request_code_service(email: str):
    user = mongo.db.users.find_one({'email': email})

    if user:
        code = generate_code()
        cache.set(code, str(user.get('_id')), timeout=1800)

        # TODO I would do it would celery, but I don't see the point of doing it in a test task
        sent_email_thread = Thread(target=send_email,
                                   args=[current_app._get_current_object(),
                                         user.get('email'),
                                         'auth@utair.com',
                                         'Auth code',
                                         code])
        sent_email_thread.start()

        return {'status': True, 'message': 'Email sent'}

    return None


def code_sign_in_service(code: str):
    user_id = cache.get(code)

    if not user_id:
        return None

    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    if not user:
        return None

    tokens = create_tokens(user_id=user_id)
    cache.set(user_id, user.get('roles'))

    return tokens


def create_tokens(user_id: str):
    config = current_app.config
    access_expires = config.get('JWT_ACCESS_TOKEN_EXPIRES')
    refresh_expires = config.get('JWT_REFRESH_TOKEN_EXPIRES')
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)
    access_jti = get_jti(encoded_token=access_token)
    refresh_jti = get_jti(encoded_token=refresh_token)
    cache.set(access_jti, refresh_jti, int(access_expires.total_seconds() * 1.2))
    cache.set(refresh_jti, access_jti, int(refresh_expires.total_seconds() * 1.2))
    tokens = {
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    return tokens


def sign_in_service(email: str, password: str):
    user = mongo.db.users.find_one({'email': email})

    if not user:
        return None

    user_password = user.get('password')

    if not user_password:
        return None

    is_correct_password = check_password_hash(user_password, password)

    if not is_correct_password:
        return None

    user_id = str(user.get('_id'))
    tokens = create_tokens(user_id=user_id)
    cache.set(user_id, user.get('roles'))

    return tokens


def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_user_id = get_jwt_identity()

            if not current_user_id:
                return abort(401)

            if not cache.get(current_user_id):
                return abort(401)

            if cache.get(current_user_id) not in roles:
                return abort(403)

            return f(*args, **kwargs)

        return wrapped

    return wrapper


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token.get('jti')

    if not jti:
        return True

    token = cache.get(jti)

    if token:
        return False

    return True
