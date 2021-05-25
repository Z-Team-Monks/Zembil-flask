from flask import Flask
from flask_restful import Resource, Api, reqparse, abort 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from zembil.config import Config


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    jwt = JWTManager(app)

    api = Api(app)
    
    db.init_app(app)

    from zembil.models import RevokedTokenModel
    
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        token = db.session.query(RevokedTokenModel.id).filter_by(jti=jti).scalar()
        return token is not None

    from zembil.resources.user import User, Users, Authorize, UserLogout
    from zembil.resources.shop import Shop, Shops
    from zembil.resources.category import Category, Categories
    from zembil.resources.location import Location, Locations
    from zembil.resources.brand import Brand, Brands
    from zembil.resources.shoplike import ShopLike
    from zembil.resources.review import Reviews, Review, ProductReviews
    from zembil.resources.wishlist import WishLists
    from zembil.resources.product import Product, Products

    api.add_resource(Users, '/api/users')
    api.add_resource(User, '/api/users/<int:id>')
    api.add_resource(Authorize, '/api/users/auth')
    api.add_resource(UserLogout, '/api/users/logout')
    api.add_resource(Categories, '/api/categories')
    api.add_resource(Category, '/api/categories/<int:id>')
    api.add_resource(Locations, '/api/locations')
    api.add_resource(Location, '/api/locations/<int:id>')
    api.add_resource(Shops, '/api/shops')
    api.add_resource(Shop, '/api/shops/<int:id>')
    api.add_resource(ShopLike, '/api/shops/<int:id>/likes')
    api.add_resource(Reviews, '/api/products/reviews')
    api.add_resource(Review, '/api/products/reviews/<int:id>')
    api.add_resource(ProductReviews, '/api/products/<int:product_id>/reviews/')
    api.add_resource(Products, '/api/products')
    api.add_resource(Product, '/api/products/<int:id>')
    api.add_resource(Brand, '/api/brands/<int:id>')
    api.add_resource(Brands, '/api/brands')

    return app
