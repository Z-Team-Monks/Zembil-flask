from flask_restful import Resource, fields, reqparse, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import ShopModel
from zembil.schemas import ShopSchema
from zembil.common.util import cleanNullTerms

shop_schema = ShopSchema()
shops_schema = ShopSchema(many=True)

shop_post_arguments = reqparse.RequestParser()
shop_post_arguments.add_argument('buildingname', type=str, help="Building name is required", required=True)
shop_post_arguments.add_argument('phonenumber1', type=str, help="Phone Number 1", required=True)
shop_post_arguments.add_argument('phonenumber2', type=str, help="Phone Number 2", required=False)
shop_post_arguments.add_argument('categoryid', type=int, help="Category Id", required=False)
shop_post_arguments.add_argument('locationid', type=int, help="Location Id", required=False)
shop_post_arguments.add_argument('description', type=str, help="Description", required=False)

shop_put_arguments = reqparse.RequestParser()
shop_put_arguments.add_argument("id", type=int, help="Shop id is required", required=True)
shop_put_arguments.add_argument('buildingname', type=str, help="Building name is required", required=False)
shop_put_arguments.add_argument('phonenumber1', type=str, help="Phone Number 1", required=False)
shop_put_arguments.add_argument('phonenumber2', type=str, help="Phone Number 2", required=False)
shop_put_arguments.add_argument('categoryid', type=int, help="Category Id", required=False)
shop_put_arguments.add_argument('locationid', type=int, help="Location Id", required=False)
shop_put_arguments.add_argument('description', type=str, help="Description", required=False)


class Shops(Resource):
    def get(self):
        result = ShopModel.query.all()
        return shops_schema.dump(result)

    @jwt_required()
    def post(self):
        args = shop_post_arguments.parse_args()
        user_id = get_jwt_identity()
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

    @jwt_required()
    def patch(self):
        args = cleanNullTerms(shop_put_arguments.parse_args())
        user_id = get_jwt_identity()
        if user_id:
            shop = ShopModel.query.filter_by(id=args['id']).update(args)
            db.commit()
        else:
            abort(403, message="User is not owner of this shop")

class Shop(Resource):
    def get(self, id):
        result = ShopModel.query.filter_by(id=id).first()
        return shop_schema.dump(result)
    