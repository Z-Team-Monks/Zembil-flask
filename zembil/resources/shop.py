import jwt
import json
from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import db
from zembil.models import ShopModel, UserModel, LocationModel, CategoryModel
from zembil.common.util import token_required
from zembil.schemas import ShopSchema

shop_schema = ShopSchema()
shop_schemas = ShopSchema(many=True)

shop_post_arguments = reqparse.RequestParser()
shop_post_arguments.add_argument('Authorization', type=str, help="Token is required", required=True, location='headers')
shop_post_arguments.add_argument('buildingname', type=str, help="Building name is required", required=True)
shop_post_arguments.add_argument('phonenumber1', type=str, help="Phone Number 1", required=True)
shop_post_arguments.add_argument('phonenumber2', type=str, help="Phone Number 2", required=False)
shop_post_arguments.add_argument('categoryid', type=int, help="Category Id", required=False)
shop_post_arguments.add_argument('locationid', type=int, help="Location Id", required=False)
shop_post_arguments.add_argument('description', type=str, help="Description", required=False)


class Shop(Resource):
    def get(self, id):
        result = ShopModel.query.filter_by(id=id).first()
        return shop_schema.dump(result)

    def post(self):
        args = shop_post_arguments.parse_args()
        token = args['Authorization'].split()[1]
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms="HS256")
            user_id = payload['user_id']
            role = payload['role']
        except:
            print("Authorization failed!")
            user_id = None
        if user_id:
            shop = ShopModel(
                user_id=user_id, 
                building_name=args['buildingname'],
                phone_number1=args['phonenumber1'],
                category_id=args['categoryid'],
                location_id=args['locationid'],
                description=args['description'])
            db.session.add(shop)
            db.session.commit()
            return shop_schema.dump(shop), 201
        else:
            return abort(404, message="User Doesn't Exist")

    def put(self):
        pass

class ShopList(Resource):
    def get(self):
        result = ShopModel.query.all()
        return result