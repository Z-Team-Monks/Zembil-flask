from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from flask_jwt_extended import ( create_access_token, get_jwt, 
    create_refresh_token, jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import UserModel, RevokedTokenModel
from zembil.schemas import UserSchema

user_schema = UserSchema()

user_post_arguments = reqparse.RequestParser()
user_post_arguments.add_argument('username', type=str, help="Username is Required", required=True)
user_post_arguments.add_argument('email', type=str, help="Email is Required", required=True)
user_post_arguments.add_argument('password', type=str, help="password is Required", required=True)
user_post_arguments.add_argument('role', type=str, help="role is Required", required=True)
user_post_arguments.add_argument('phone', type=str, help="role is Required", required=True)

user_update_arguments = reqparse.RequestParser()
user_update_arguments.add_argument("username", type=str, required=False)
user_update_arguments.add_argument("phone", type=str, required=False)

user_auth_arguments = reqparse.RequestParser()
user_auth_arguments.add_argument('username', type=str, help="Username is Required", required=True)
user_auth_arguments.add_argument('password', type=str, help="password is Required", required=True)

class Users(Resource):
    def post(self):
        args = user_post_arguments.parse_args()
        user = UserModel(username=args['username'], email=args['email'], password=args['password'], role=args['role'], phone=args['phone'])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201

    @jwt_required()
    def patch(self):
        args = user_post_arguments.parse_args()
        user_id = get_jwt_identity()
        existing = UserModel.query.filter_by(id=user_id).first()
        if existing:
            if args['username']:
                existing.username = args['username']
            if args['phone']:
                existing.phone = args['phone']
            db.session.commit() 
            return user_schema.dump()
        return abort(403, message="User not authorized!")

class User(Resource):
    @jwt_required()
    def get(self, id):
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found!")
        return user_schema.dump(result)

class Authorize(Resource):
    def post(self):
        args = user_auth_arguments.parse_args()
        username = args['username']
        password = args['password']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            additional_claims = {"role": user.role}
            token = create_access_token(identity=user.id, additional_claims=additional_claims)
            return {'token': token}
        return abort(401, message="Incorrect Username or password")

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            db.session.add(revoked_token)
            db.session.commit()
            return {'message': 'User log out succesfull'}, 200
        except:
            return {'message': 'Something went wrong'}, 500
