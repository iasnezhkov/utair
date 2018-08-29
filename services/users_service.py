from bson import ObjectId
from flask_jwt_extended import get_jwt_identity

from extensions import mongo


def get_profile_service():
    current_user = get_jwt_identity()

    if not current_user:
        return None

    user = mongo.db.users.find_one({'_id': ObjectId(current_user)}, {'_id': False, 'password': False})

    if not user:
        return None

    return user
