import datetime
import os

APP_ROOT_FOLDER = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))))

settings = {
    'MONGO_URI': 'mongodb://localhost:27017/utair',

    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 86400,

    'JWT_ACCESS_TOKEN_EXPIRES': datetime.timedelta(days=1),
    'JWT_REFRESH_TOKEN_EXPIRES': datetime.timedelta(days=30),
    'JWT_BLACKLIST_ENABLED': True,
    'JWT_BLACKLIST_TOKEN_CHECKS': ['access', 'refresh'],
    'JWT_TOKEN_LOCATION': 'headers',
    'JWT_HEADER_NAME': 'Authorization',
    'JWT_HEADER_TYPE': 'Bearer',
    'JWT_ALGORITHM': 'HS256',
    'JWT_SECRET_KEY': 'test',
    'JWT_IDENTITY_CLAIM': 'identity',
    'JWT_USER_CLAIMS': 'user_claims',

    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 465,
    'MAIL_USE_SSL': True,
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME', 'blank'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD', 'blank'),

    'APP_ROOT_FOLDER': APP_ROOT_FOLDER,
    'SECRET_KEY': 'test',

    'DATE_FORMAT': '%a, %d %b %Y %H:%M:%S GMT',
}
