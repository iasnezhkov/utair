from flask import request, jsonify

from blueprints import auth
from controllers.auth_controller import request_code_controller, code_sign_in_controller, sign_in_controller
from extensions import limiter


@auth.route('/request-code', methods=['POST'])
def request_code_route():
    request_json = request.json
    result, status_code = request_code_controller(data=request_json)

    return jsonify(result), status_code


@auth.route('/code-sign-in', methods=['POST'])
@limiter.limit('10/minute')
def code_sign_in_route():
    request_json = request.json
    result, status_code = code_sign_in_controller(request_json)

    return jsonify(result), status_code


@auth.route('/sign-in', methods=['POST'])
@limiter.limit('10/minute')
def sign_in_route():
    request_json = request.json
    result, status_code = sign_in_controller(request_json)

    return jsonify(result), status_code
