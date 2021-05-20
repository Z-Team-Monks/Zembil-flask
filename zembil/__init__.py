from flask import Flask
from flask_restful import Resource, Api, reqparse, abort 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from zembil.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    
    db.init_app(app)

    from zembil.resources.user import User, Authorize

    api.add_resource(User, '/api/users', '/api/users/<int:id>')
    api.add_resource(Authorize, '/api/users/auth')

    return app
