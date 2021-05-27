from flask import Blueprint
from flask_restful import Api
from zembil.resources.v1.user import User, Users, Authorize, UserLogout
from zembil.resources.v1.shop import Shop, Shops, SearchShop
from zembil.resources.v1.category import Category, Categories
from zembil.resources.v1.location import Location, Locations
from zembil.resources.v1.brand import Brand, Brands
from zembil.resources.v1.shoplike import ShopLike, ShopLikes
from zembil.resources.v1.review import Reviews, Review
from zembil.resources.v1.wishlist import WishLists, WishList
from zembil.resources.v1.product import Product, Products, ShopProducts, SearchProduct

API_VERSION_V1=1
API_VERSION=API_VERSION_V1
api_v1_bp = Blueprint('api_v1', __name__)
api_v1 = Api(api_v1_bp)


api_v1.add_resource(Users, '/users')
api_v1.add_resource(User, '/users/<int:id>')
api_v1.add_resource(Authorize, '/auth')
api_v1.add_resource(UserLogout, '/users/logout')

api_v1.add_resource(Categories, '/categories')
api_v1.add_resource(Category, '/categories/<int:id>')

api_v1.add_resource(Locations, '/locations')
api_v1.add_resource(Location, '/locations/<int:id>')

api_v1.add_resource(Shops, '/shops')
api_v1.add_resource(Shop, '/shops/<int:id>')
api_v1.add_resource(ShopLikes, '/shops/<int:shopid>/likes')
api_v1.add_resource(ShopLike, '/shops/<int:shopid>/likes/<int:id>')
api_v1.add_resource(ShopProducts, '/shops/<int:shop_id>/products')

api_v1.add_resource(Reviews, '/products/<int:product_id>/reviews')
api_v1.add_resource(Review, '/products/<int:product_id>/reviews/<int:id>')
api_v1.add_resource(Products, '/products')
api_v1.add_resource(Product, '/products/<int:id>')

api_v1.add_resource(SearchProduct, '/search/products')
api_v1.add_resource(SearchShop, '/search/shops')

api_v1.add_resource(Brand, '/brands/<int:id>')
api_v1.add_resource(Brands, '/brands')

api_v1.add_resource(WishLists, '/users/<int:user_id>/cart/<int:id>')
api_v1.add_resource(WishList, '/users/<int:user_id>/cart')