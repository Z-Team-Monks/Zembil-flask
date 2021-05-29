from flask import request
from flask_restx import Resource, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from marshmallow import ValidationError
from zembil import db
from zembil.models import UserModel, ShopModel, LocationModel, CategoryModel
from zembil.schemas import ShopSchema, LocationSchema
from zembil.common.util import cleanNullTerms

shop_schema = ShopSchema()
location_schema = LocationSchema()

shops_schema = ShopSchema(many=True)

class Shops(Resource):
    def get(self):
        result = ShopModel.query.all()
        return shops_schema.dump(result)

    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            location_args = location_schema.load(data['location'])
            shop_args = shop_schema.load(data['shop'])
        except ValidationError as errors:
            abort(400, message=errors.messages)
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if user:
            try:
                location = LocationModel(
                    **location_args
                )
                db.session.add(location)
                db.session.commit()
            except:
                abort(500, message="Database error")
            try:
                shop = ShopModel(
                    user_id=user_id,
                    location_id=location.id, 
                    **shop_args)
                db.session.add(shop)
                db.session.commit()
            except:
                abort(500, message="Database error")
            
            return shop_schema.dump(shop), 201
        abort(404, message="User Doesn't Exist")


class Shop(Resource):
    def get(self, id):
        result = ShopModel.query.filter_by(id=id).first()
        if result:
            return shop_schema.dump(result)
        abort(404, message="Shop Doesn't Exist")
    
    @jwt_required()
    def patch(self, id):
        data = request.get_json()
        try:
            args = ShopSchema(partial=True).load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        args = cleanNullTerms(args)
        if not args:
            abort(400, message="Empty json body")
        user = get_jwt_identity()
        existing = ShopModel.query.get(id)
        if existing and user.id == existing.user_id:
            shop = ShopModel.query.filter_by(id=id).update(args)
            db.session.commit()
            query = ShopModel.query.get(id)
            return shop_schema.dump(query), 200
        if existing:
            abort(403, message="User is not owner of this shop")
        abort(404, message="Shop doesn't exist!")

    def delete(self, id):
        shop = ShopModel.query.get(id)
        if shop:
            db.session.delete(shop)
            db.session.commit()
            return 204
        return abort(404, message="Shop doesn't exist!")

class SearchShop(Resource):
    def get(self):
        name = request.args.get('name')
        category = request.args.get('category')
        shops = ShopModel.query
        if name:
            shops = shops.filter(ShopModel.name.ilike('%' + name + '%'))
        if category:
            shops = shops.filter(CategoryModel.name.ilike('%' + category + '%'))
        shops = shops.order_by(ShopModel.name).all()
        if shops:
            return products_schema.dump(products)
        abort(404, message="Product doesn't exist!")

class ApproveShop(Resource):
    @jwt_required()
    def put(self, id):
        role = get_jwt()['role']
        if role == 'user':
            abort(403, message="Higher Privelege required")
        shop = ShopModel.query.get(id)
        shop.is_approved = True
        db.session.commit()
        return 204
