from flask import jsonify, request
from flask_jwt_extended import jwt_required

from blueprints import transactions
from controllers.transactions_controller import create_transaction_controller, get_transactions_controller
from services.auth_service import required_roles


@transactions.route('', methods=['POST'])
@jwt_required
@required_roles(['service'])
def create_transaction_route():
    request_json = request.json
    result, status_code = create_transaction_controller(request_json)

    return jsonify(result), status_code


@transactions.route('', methods=['GET'])
@jwt_required
def get_transactions_route():
    url_params = request.args
    result, status_code = get_transactions_controller(url_params)

    return jsonify(result), status_code
