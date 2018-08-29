from flask import jsonify
from flask_jwt_extended import jwt_required

from blueprints import users
from controllers.users_controller import get_profile_controller


@users.route('/me', methods=['GET'])
@jwt_required
def get_profile_route():
    result, status_code = get_profile_controller()

    return jsonify(result), status_code
