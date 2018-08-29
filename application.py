from flask import Flask
from importlib import import_module

from settings import settings
from extensions import mail, mongo, cache, jwt, limiter
from blueprints import http_blueprints
from management.commands import populate_users_command, populate_transactions_command


def create_app():
    application = Flask(__name__)
    application.config.update(settings)

    mail.init_app(application)
    mongo.init_app(application)
    cache.init_app(application)
    jwt.init_app(application)
    limiter.init_app(application)

    for bp in http_blueprints:
        import_module(bp.import_name)
        application.register_blueprint(bp)

    application.cli.add_command(populate_users_command)
    application.cli.add_command(populate_transactions_command)

    return application
