from flask import request
from flask_restful import Resource, fields, reqparse, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import ShopLikeModel, ShopModel
from zembil.schemas import ShopLikeSchema, TotalShopLikeSchema

shoplike_schema = ShopLikeSchema()
shoplikes_schema = TotalShopLikeSchema()

class ShopLikes(Resource):
    def get(self, shopid):
        shoplike = ShopModel.query.get(shopid)
        if shoplike:
            return shoplikes_schema.dump(shoplike)
        return abort(404, message="No Shop Likes Found")
    
    @jwt_required()
    def post(self, shopid):
        user_id = get_jwt_identity()
        existing = ShopLikeModel.query.filter_by(user_id=user_id, shop_id=shopid).first()
        if not existing:
            shoplike = ShopLikeModel(user_id=user_id, shop_id=shopid)
            db.session.add(shoplike)
            db.session.commit()
            return shoplike_schema.dump(shoplike), 201
        return abort(409, message="User already")


class ShopLike(Resource):
    @jwt_required()
    def delete(self, shopid, id):
        user_id = get_jwt_identity()
        existing = ShopLikeModel.query.get(id)
        if existing and existing.user_id == user_id:
            db.session.delete(existing)
            db.session.commit()
            return 200
        if existing:
            abort(401, "Can't delete!")
        abort(404, "Doesn't exist")



    