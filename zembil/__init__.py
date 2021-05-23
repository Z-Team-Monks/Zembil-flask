from flask import Flask
from flask_restful import Resource, Api, reqparse, abort 
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from zembil.config import Config

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    
    db.init_app(app)

    from zembil.resources.user import User, Authorize
    from zembil.resources.shop import Shop, ShopList
    from zembil.resources.category import Category
    from zembil.resources.location import Location

    api.add_resource(User, '/api/users', '/api/users/<int:id>')
    api.add_resource(Authorize, '/api/users/auth')
    api.add_resource(Categories, '/api/categories')
    api.add_resource(category, '/api/categories/<int:id>')
    api.add_resource(Locations, '/api/locations')
    api.add_resource(Location, '/api/locations/<int:id>')
    api.add_resource(Shops, '/api/shops')
    api.add_resource(Shop, '/api/shops/<int:id>')
    api.add_resource(ShopLikes, '/api/shoplikes')
    api.add_resource(ShopLike, '/api/shoplikes/<int:id>')

    return app
