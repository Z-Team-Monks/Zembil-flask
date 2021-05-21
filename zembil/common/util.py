import jwt
from functools import wraps
from flask import current_app, request

def user_token_required(fun):
    @wraps(fun)
    def decorated(*args, **kwargs):
        try:
            headers = request.headers
            bearer = headers.get('Authorization')    # Bearer YourTokenHere
            token = bearer.split()[1]  # YourTokenHere
            print(token)
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
        except:
            return {'message': 'Unauthorized user!'}, 403
        
        return fun(*args, **kwargs)
    return decorated

def shop_user_token_required(fun):
    @wraps(fun)
    def decorated(*args, **kwargs):
        try:
            headers = request.headers
            bearer = headers.get('Authorization')    # Bearer YourTokenHere
            token = bearer.split()[1]  # YourTokenHere
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            if data['role'] != 'shop_owner':
                return {'message': 'Higher privilege required!'}, 403
        except:
            return {'message': 'Unauthorized user!'}, 403
        
        return fun(*args, **kwargs)
    return decorated

def admin_token_required(fun):
    @wraps(fun)
    def decorated(*args, **kwargs):
        try:
            headers = request.headers
            bearer = headers.get('Authorization')    # Bearer YourTokenHere
            token = bearer.split()[1]  # YourTokenHere
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            if data['role'] != 'admin':
                return {'message': 'Higher privilege required!'}, 403
        except:
            return {'message': 'Unauthorized user!'}, 403
        
        return fun(*args, **kwargs)
    return decorated

def get_user_from_token(bearer):
    try:
        token = bearer.split()[1]
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
        user_id = payload['user_id']
        role = payload['role']
    except:
        print("Authorization failed!")
        user_id = None
        role = None
    return user_id, role
