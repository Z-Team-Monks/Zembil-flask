from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS
from zembil.resources.v1.user import User, Users, Authorize, UserLogout, AdminUser
from zembil.resources.v1.shop import Shop, Shops, SearchShop, ApproveShop
from zembil.resources.v1.category import Category, Categories
from zembil.resources.v1.location import Location, Locations, LocationNearMe
from zembil.resources.v1.shopfollow import ShopFollower, ShopFollowers
from zembil.resources.v1.review import Reviews, Review
from zembil.resources.v1.wishlist import WishLists, WishList
from zembil.resources.v1.product import Product, Products, ShopProducts, SearchProduct, TrendingProduct, FilterProduct
from zembil.resources.v1.advertisement import Advertisements, Advertisement
from zembil.resources.v1.upload import UploadShopImage, UploadProductImage

API_VERSION_V1=1
API_VERSION=API_VERSION_V1
api_v1_bp = Blueprint('api_v1', __name__)
CORS(api_v1_bp, supports_credentials=True)
api_v1 = Api(api_v1_bp)

api_v1.add_resource(Users, '/users')
api_v1.add_resource(User, '/users/<int:id>')
api_v1.add_resource(Authorize, '/auth')
api_v1.add_resource(UserLogout, '/users/logout')
api_v1.add_resource(AdminUser, '/admin')

api_v1.add_resource(Categories, '/categories')
api_v1.add_resource(Category, '/categories/<int:id>')

api_v1.add_resource(Locations, '/locations')
api_v1.add_resource(Location, '/locations/<int:id>')

api_v1.add_resource(Shops, '/shops')
api_v1.add_resource(Shop, '/shops/<int:id>')
api_v1.add_resource(ShopProducts, '/shops/<int:shop_id>/products')
api_v1.add_resource(ApproveShop, '/shops/<int:id>/status')
api_v1.add_resource(ShopFollowers, '/shops/<int:shopid>/followers')
api_v1.add_resource(ShopFollower, '/shops/<int:shopid>/followers/<int:id>')
api_v1.add_resource(LocationNearMe, '/shops/nearme')
api_v1.add_resource(UploadShopImage, '/shops/<int:shop_id>/upload')

api_v1.add_resource(Reviews, '/products/<int:product_id>/reviews')
api_v1.add_resource(Review, '/products/<int:product_id>/reviews/<int:id>')
api_v1.add_resource(Products, '/products')
api_v1.add_resource(Product, '/products/<int:id>')
api_v1.add_resource(TrendingProduct, '/products/trending')
api_v1.add_resource(UploadProductImage, '/products/<int:product_id>/upload')

api_v1.add_resource(FilterProduct, '/filter/products')
api_v1.add_resource(SearchProduct, '/search/products')
api_v1.add_resource(SearchShop, '/search/shops')

api_v1.add_resource(WishList, '/cart/<int:id>')
api_v1.add_resource(WishLists, '/cart')

api_v1.add_resource(Advertisement, '/ads')
api_v1.add_resource(Advertisements, '/ads/<int:id>')