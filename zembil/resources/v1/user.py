from datetime import timedelta
from flask import current_app, request
from flask_restful import Resource, fields, abort, reqparse
from flask_jwt_extended import ( create_access_token, get_jwt,
                            jwt_required, get_jwt_identity)
from marshmallow import ValidationError
from zembil import db
from zembil.models import UserModel, RevokedTokenModel
from zembil.schemas import UserSchema
from zembil.common.util import cleanNullTerms

user_schema = UserSchema()

user_auth_arguments = reqparse.RequestParser()
user_auth_arguments.add_argument('username', type=str, help="Username", required=True)
user_auth_arguments.add_argument('password', type=str, help="Password", required=True)

class Users(Resource):
    def post(self):
        data = request.get_json()
        try:
            args = user_schema.load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        user = UserModel(username=args['username'], email=args['email'], password=args['password_hash'], role=args['role'], phone=args['phone'])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user), 201


class User(Resource):
    @jwt_required()
    def get(self, id):
        result = UserModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="User not found!")
        return user_schema.dump(result)

    @jwt_required()
    def patch(self, id):
        data = request.get_json()
        try:
            args = UserSchema(partial=True).load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        args = cleanNullTerms(args)
        user_id = get_jwt_identity()
        if user == id:
            existing = UserModel.query.filter_by(id=id).update(args)
        return abort(403, message="User not authorized!")


class Authorize(Resource):
    def post(self):
        args = user_auth_arguments.parse_args()
        username = args['username']
        password = args['password']
        user = UserModel.query.filter_by(username=username).first()
        if user and user.check_password(password):
            expires = timedelta(days=30)
            additional_claims = {"role": user.role}
            token = create_access_token(
                identity=user.id, 
                expires_delta=expires,
                additional_claims=additional_claims)
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
