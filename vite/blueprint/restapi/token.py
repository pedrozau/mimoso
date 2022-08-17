from flask import request, jsonify
from dynaconf import settings
from functools import wraps
import datetime
import jwt






SECRET_KEY = settings.get("SECRET_KEY")


def generate_token(user_name):

    return jwt.encode({'email': user_name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=300)}, SECRET_KEY)



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        try:
          
            token = request.get_json()
          
            if not token['token']:
                return jsonify({'message_error': 'Token is missing'})
            try:
                data = jwt.decode(token['token'], SECRET_KEY,algorithms=['HS256'])
            except Exception as error:
                print(error)
                return jsonify({'message_error': 'Token is invalid'})

            return f(*args, **kwargs)
        except TypeError:
            return jsonify({
                "messsage_error": "Token is Missing"
            })
        except Exception:
            return jsonify({
                "message_error":"informe the token"
            })
    return decorated


