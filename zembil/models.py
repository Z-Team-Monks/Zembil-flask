from datetime import datetime
from zembil import db, bcrypt

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(50), nullable=True)

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class ShopModel(db.Model):
    __tablename__ = "shop"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    building_name = db.Column(db.String(100), nullable=False)
    phone_number1 = db.Column(db.String(10), nullable=True)
    phone_number1 = db.Column(db.String(10), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)

class ProductModel(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    building_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    delivery_available = db.Column(db.Boolean, nullable=False, default=True)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    product_count = db.Column(db.Integer, nullable=False, default=1)
    __table_args__ = (db.UniqueConstraint('shop_id', 'name'), )


class CategoryModel(db.Model):
    __tablename__ = "category"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

class BrandModel(db.Model):
    __tablename__ = "brand"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

class LocationModel(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    longtitude = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    __table_args__ = (db.UniqueConstraint('latitude', 'longtitude'), )

class ReviewModel(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_review = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id'), )

class WishListModel(db.Model):
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id'), )

class ShopLikeModel(db.Model):
    __tablename__ = "shop_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'shop_id'), )
