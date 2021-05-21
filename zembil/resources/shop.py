import jwt
import json
from flask import current_app
from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import db
from zembil.models import ShopModel, UserModel, LocationModel, CategoryModel
from zembil.common.util import user_token_required, shop_user_token_required
from zembil.schemas import ShopSchema

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)

shop_post_arguments = reqparse.RequestParser()
shop_post_arguments.add_argument('Authorization', type=str, help="Token is required", required=True, location='headers')
shop_post_arguments.add_argument('buildingname', type=str, help="Building name is required", required=True)
shop_post_arguments.add_argument('phonenumber1', type=str, help="Phone Number 1", required=True)
shop_post_arguments.add_argument('phonenumber2', type=str, help="Phone Number 2", required=False)
shop_post_arguments.add_argument('categoryid', type=int, help="Category Id", required=False)
shop_post_arguments.add_argument('locationid', type=int, help="Location Id", required=False)
shop_post_arguments.add_argument('description', type=str, help="Description", required=False)

shop_put_arguments = reqparse.RequestParser()
shop_put_arguments.add_argument('Authorization', type=str, help="Token is required", required=True, location='headers')
shop_put_arguments.add_argument("id", type=int, help="Shop id is required", required=True)
shop_put_arguments.add_argument('buildingname', type=str, help="Building name is required", required=False)
shop_put_arguments.add_argument('phonenumber1', type=str, help="Phone Number 1", required=False)
shop_put_arguments.add_argument('phonenumber2', type=str, help="Phone Number 2", required=False)
shop_put_arguments.add_argument('categoryid', type=int, help="Category Id", required=False)
shop_put_arguments.add_argument('locationid', type=int, help="Location Id", required=False)
shop_put_arguments.add_argument('description', type=str, help="Description", required=False)


class ShopList(Resource):
    def get(self):
        result = ShopModel.query.all()
        return shops_schema.dump(result)

    @user_token_required
    def post(self):
        args = shop_post_arguments.parse_args()
        user_id, _ = get_user_from_token(args['Authorization'])
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

    @user_token_required
    def put(self):
        args = shop_put_arguments.parse_args()
        user_id, _ = get_user_from_token(args['Authorization'])
        if user_id:
            shop = ShopModel.query.filter_by(id=args['id'])
            if user_id == shop.user_id:
                pass
            else:
                abort(403, message="User is not owner of this shop")

class Shop(Resource):
    def get(self, id):
        result = ShopModel.query.filter_by(id=id).first()
        return shop_schema.dump(result)
    