from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import ShopFollowerModel, ShopModel
from zembil.schemas import ShopFollowerSchema, TotalShopFollowerSchema

shopfollower_schema = ShopFollowerSchema()
shopfollowers_schema = TotalShopFollowerSchema()

class ShopFollowers(Resource):
    def get(self, shopid):
        shopfollow = ShopModel.query.get(shopid)
        if shopfollow:
            return shopfollowers_schema.dump(shopfollow)
        return abort(404, message="No Shop Followers Found")
    
    @jwt_required()
    def post(self, shopid):
        user_id = get_jwt_identity()
        existing = ShopFollowerModel.query.filter_by(user_id=user_id, shop_id=shopid).first()
        if not existing:
            shopfollow = ShopFollowerModel(user_id=user_id, shop_id=shopid)
            db.session.add(shopfollow)
            db.session.commit()
            return shopfollower_schema.dump(shopfollow), 201
        return abort(409, message="User already is following this shop")


class ShopFollower(Resource):
    @jwt_required()
    def delete(self, shopid, id):
        user_id = get_jwt_identity()
        existing = ShopFollowerModel.query.get(id)
        if existing and existing.user_id == user_id:
            db.session.delete(existing)
            db.session.commit()
            return {"message": "Successfull"}, 204
        if existing:
            abort(401, "Can't delete!")
        abort(404, "Doesn't exist")
