from flask import request
from flask_restful import Resource, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import WishListModel
from zembil.schemas import WishListSchema

wishlist_schema = WishListSchema()
wishlists_schema = WishListSchema(many=True)

class WishLists(Resource):
    def get(self):
        user_id = get_jwt_identity()
        wishlists = WishListModel.query.filter_by(user_id=user_id)
        if wishlists:
            return wishlists_schema.dump(wishlists)
        return abort(404, "No wish list found for this user")

    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            args = wishlist_schema.load(data, partial=("product_id",))
        except ValidationError as errors:
            abort(400, message=errors.messages)
        user_id = get_jwt_identity()
        existing = WishListModel.query.filter_by(user_id=user_id, product_id=args['productid']).first()
        if not existing:
            wishlist = WishListModel(
                product_id=args['product_id'],
                user_id=user_id,
            )
            db.session.add(wishlist)
            db.session.commit()
            return wishlist_schema.dump(wishlist)
        return abort(409, "Product already exists in wishlist")
    

class WishList(Resource):
    def get(self, id):
        user_id = get_jwt_identity()
        wishlist = WishListModel.query.filter_by(id=id).first()
        if wishlist:
            return wishlist_schema.dump(wishlist)
        return abort(404, "No wishlist item found for this user")

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()
        existing = WishListModel.query.filter_by(id=id, user_id=user_id).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            return wishlist_schema.dump(existing)
        return abort(404, "No wishlist item found with this id!")

