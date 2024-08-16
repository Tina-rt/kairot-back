from flask import request
from functools import wraps
import jwt
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Missing token'}, 400
        try:
            data = jwt.decode(token, options={"verify_signature": False})
            current_user = data
        except Exception as e:
            print(e)
            return {'error': 'Invalid token'}, 400
            
        return f(current_user, *args, **kwargs)
    return decorated
    