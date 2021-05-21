import jwt
from functools import wraps
from flask import current_app, request

def token_required(fun):
    @wraps(fun)
    def decorated(*args, **kwargs):
        headers = request.headers
        bearer = headers.get('Authorization')    # Bearer YourTokenHere
        token = bearer.split()[1]  # YourTokenHere
        # token = request.args.get('token')

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return {'message': 'Invalid token!'}
        
        return fun(*args, **kwargs)
    return decorated