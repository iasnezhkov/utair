from flask import Blueprint

URL_PREFIX = '/api/v1/'


def _factory(partial_module_string, url_prefix):
    name = partial_module_string
    import_name = 'routes.{}'.format(partial_module_string)
    blueprint = Blueprint(name, import_name, url_prefix=URL_PREFIX + url_prefix)
    return blueprint


users = _factory('users_route', 'users')
transactions = _factory('transactions_route', 'transactions')
auth = _factory('auth_route', 'auth')
http_blueprints = (users, transactions, auth,)
