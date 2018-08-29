from services.users_service import get_profile_service


def get_profile_controller():
    user_info = get_profile_service()

    if not user_info:
        return {'status': False, 'error': 'user not exists'}, 404

    return user_info, 200
