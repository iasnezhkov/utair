from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_caching import Cache
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

mail = Mail()
mongo = PyMongo()
cache = Cache()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)
