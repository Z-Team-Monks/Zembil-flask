from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    #  id, username, email, password, role, phone
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String, nullable=True)

class Product(db.Model):
    __tablename__ = "product"
    #  id, shop_id, name, date, building_name, description, category, price, condition, image, delivery_available, discount, product_count
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    building_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    delivery_available = db.Column(db.Boolean, nullable=False, default=True)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    product_count = db.Column(db.Integer, nullable=False, default=1)


class Category(db.Model):
    __tablename__ = "category"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class Brand(db.Model):
    __tablename__ = "brand"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class Location(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    longtitude = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_review = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class WishList(db.Model):
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class ShopLike(db.Model):
    __tablename__ = "shop_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
