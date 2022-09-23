import datetime
from functools import wraps

import jwt
from dynaconf import settings
from flask import jsonify, request

SECRET_KEY = settings.get('SECRET_KEY')


def generate_token(user_name):
    """
    Generate token for each user in system.
    """
    return jwt.encode({'email': user_name, 'exp': (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=300))}, SECRET_KEY)


def token_required(f):
    """
    Verify the token for each user in the system.
    Authorization'
    """

    @wraps(f)
    def decorated(*args, **kwargs):

        try:

            token = None
            if "Authorization" in request.headers:
                token = request.headers["Authorization"].split(" ")[1]
            if not token:
                return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
                }, 401
            try:
                return jwt.decode(
                    token, SECRET_KEY, algorithms=['HS256']
                )
            except Exception as error:
                print(error)
                return jsonify({'message_error': 'Token is invalid'})

            return f(*args, **kwargs)
        except TypeError:
            return jsonify({'messsage_error': 'Token is Missing'})
        except Exception:
            return jsonify({'message_error': 'informe the token'})

    return decorated
