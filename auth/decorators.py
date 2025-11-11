from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import current_user


def require_organizer_grant():
    """Decorator que exige que o usuário seja do tipo 'organizer'."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_organizer():
                return jsonify({'error': 'Forbidden'}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
