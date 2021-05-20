import jwt
from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import bcrypt, db
from zembil.models import UserModel

user_resource_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    # 'password_hash': fields.String,
    'role': fields.String,
    'phone': fields.String
}

authorize_resource_field = {
    'token': fields.String
}

user_put_arguments = reqparse.RequestParser()
user_put_arguments.add_argument('username', type=str, help="Username is Required", required=True)
user_put_arguments.add_argument('email', type=str, help="Email is Required", required=True)
user_put_arguments.add_argument('password', type=str, help="password is Required", required=True)
user_put_arguments.add_argument('role', type=str, help="role is Required", required=True)
user_put_arguments.add_argument('phone', type=str, help="role is Required", required=True)

# user_get_argument = reqparse.RequestParser()
# user_get_argument.add_argument('id', type=int, location='args', required=True)

user_auth_arguments = reqparse.RequestParser()
user_auth_arguments.add_argument('username', type=str, help="Username is Required", required=True)
user_auth_arguments.add_argument('password', type=str, help="password is Required", required=True)

class User(Resource):
    @marshal_with(user_resource_fields)
    def get(self, id):
        # id = user_get_argument.parse_args() 
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found!")
        return result
    
    @marshal_with(user_resource_fields)
    def post(self):
        args = user_put_arguments.parse_args()
        user = UserModel(username=args['username'], email=args['email'], password=args['password'], role=args['role'], phone=args['phone'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_resource_fields)
    def patch(self):
        pass

class Authorize(Resource):
    @marshal_with(authorize_resource_field)
    def post(self):
        args = user_auth_arguments.parse_args()
        username = args['username']
        password = args['password']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            token = jwt.encode({'user': username}, current_app.config['SECRET_KEY'])
            return {'token': token}
        return abort(401, message="Incorrect Username or password")
