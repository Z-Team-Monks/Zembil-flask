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
    api.add_resource(Category, '/api/categories', '/api/categories/<int:id>')
    api.add_resource(Location, '/api/locations', '/api/locations/<int:id>')
    api.add_resource(Shop, '/api/shops/<int:id>')
    api.add_resource(ShopList, '/api/shops')

    return app
