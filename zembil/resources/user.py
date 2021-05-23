import jwt
from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import db
from zembil.models import UserModel
from zembil.schemas import UserSchema
from zembil.common.util import admin_token_required

user_schema = UserSchema()

user_post_arguments = reqparse.RequestParser()
user_post_arguments.add_argument('username', type=str, help="Username is Required", required=True)
user_post_arguments.add_argument('email', type=str, help="Email is Required", required=True)
user_post_arguments.add_argument('password', type=str, help="password is Required", required=True)
user_post_arguments.add_argument('role', type=str, help="role is Required", required=True)
user_post_arguments.add_argument('phone', type=str, help="role is Required", required=True)

user_update_arguments = reqparse.RequestParser()
shoplike_post_arguments.add_argument('Authorization', type=str, help="Token is required", required=True, location='headers')
user_update_arguments.add_argument("username", type=str, required=False)
user_update_arguments.add_argument("phone", type=str, required=False)

user_auth_arguments = reqparse.RequestParser()
user_auth_arguments.add_argument('username', type=str, help="Username is Required", required=True)
user_auth_arguments.add_argument('password', type=str, help="password is Required", required=True)

class User(Resource):
    @admin_token_required
    def get(self, id):
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found!")
        return user_schema.dump(result)
    
    def post(self):
        args = user_post_arguments.parse_args()
        user = UserModel(username=args['username'], email=args['email'], password=args['password'], role=args['role'], phone=args['phone'])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    @user_token_required
    def patch(self):
        args = user_post_arguments.parse_args()
        user_id, _ = get_user_from_token(args['Authorization'])
        existing = UserModel.query.filter_by(id=user_id).first()
        if existing:
            if args['username']:
                existing.username = args['username']
            if args['phone']:
                existing.phone = args['phone']
            db.session.commit() 
            return user_schema.dump()
        return abort(403, message="User not authorized!")

class Authorize(Resource):
    def post(self):
        args = user_auth_arguments.parse_args()
        username = args['username']
        password = args['password']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            token = jwt.encode({'user_id': user.id, 'role': user.role}, current_app.config['SECRET_KEY'], algorithm="HS256")
            return {'token': token}
        return abort(401, message="Incorrect Username or password")
