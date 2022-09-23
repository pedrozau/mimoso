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

            token = request.headers.get("Authorization")

            if not token['token']:
                return jsonify({'message_error': 'Token is missing'})
            try:
                return jwt.decode(
                    token['token'], SECRET_KEY, algorithms=['HS256']
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
