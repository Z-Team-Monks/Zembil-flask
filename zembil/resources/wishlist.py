from flask_restful import Resource, fields, reqparse, abort
from zembil import db
from zembil.models import WishListModel
from zembil.schemas import WishListSchema
from zembil.common.util import user_token_required, get_user_from_token

wishlist_schema = WishListSchema()
wishlists_schema = WishListSchema(many=True)

wishlist_post_arguments = reqparse.RequestParser() # prodcut_id, user_Id
wishlist_post_arguments.add_argument('productid', type=int, help="Product id is required", required=True)
wishlist_post_arguments.add_argument('Authorization', type=str, help="Token is required", required=True, location='headers')


class WishLists(Resource):
    def get(self):
        args = wishlist_post_arguments.parse_args()    
        user_id, _ = get_user_from_token(args['Authorization'])
        wishlists = WishListModel.query.filter_by(user_id=user_id)
        if wishlists:
            return wishlists_schema.dump(wishlists)
        return abort(404, "No wish list found for this user")

    @user_token_required
    def post(self):
        args = wishlist_post_arguments.parse_args()
        user_id, _ = get_user_from_token(args['Authorization'])
        existing = WishListModel.query.filter_by(user_id=user_id, product_id=args['productid']).first()
        if not existing:
            wishlist = WishListModel(
                product_id=args['productid'],
                user_id=user_id,
            )
            db.session.add(wishlist)
            db.session.commit()
            return wishlist_schema.dump(wishlist)
        return abort(409, "Product already exists in wishlist")
    

class WishList(Resource):
    def get(self, id):
        args = wishlist_post_arguments.parse_args()    
        user_id, _ = get_user_from_token(args['Authorization'])
        wishlist = WishListModel.query.filter_by(id=id).first()
        if wishlist:
            return wishlist_schema.dump(wishlists)
        return abort(404, "No wishlist item found for this user")

    @user_token_required
    def delete(self, id):
        args = wishlist_post_arguments.parse_args()    
        user_id, _ = get_user_from_token(args['Authorization'])
        existing = WishListModel.query.filter_by(id=id, user_id=user_id).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            return wishlist_schema.dump(existing)
        return abort(404, "No wishlist item found with this id!")

