from datetime import datetime
from zembil import db, bcrypt

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(50), nullable=True)

    shops = db.relationship('ShopModel', back_populates='user')
    reviews = db.relationship('ReviewModel', back_populates='user')
    wishlists = db.relationship('WishListModel', back_populates='user')
    shoplikes = db.relationship('ShopLikeModel', back_populates='user')

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
    phone_number1 = db.Column(db.String(50), nullable=True)
    phone_number2 = db.Column(db.String(50), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)

    user = db.relationship('UserModel', back_populates='shops')
    location = db.relationship('LocationModel', back_populates='shop')
    category = db.relationship('CategoryModel', back_populates='shops')
    products = db.relationship('ProductModel', back_populates='shop')
    shoplikes = db.relationship('ShopLikeModel', back_populates='shop')

class ProductModel(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    delivery_available = db.Column(db.Boolean, nullable=False, default=False)
    discount = db.Column(db.Float, nullable=False, default=0.0)
    product_count = db.Column(db.Integer, nullable=False, default=1)
    __table_args__ = (db.UniqueConstraint('shop_id', 'name'), )

    shop = db.relationship('ShopModel', back_populates='products')
    brand = db.relationship('BrandModel', back_populates='products')
    wishlists = db.relationship('WishListModel', back_populates='product')
    reviews = db.relationship('ReviewModel', back_populates='product')
    category = db.relationship('CategoryModel', back_populates='products')

class CategoryModel(db.Model):
    __tablename__ = "category"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    shops = db.relationship('ShopModel', back_populates='category')
    products = db.relationship('ProductModel', back_populates='category')

class BrandModel(db.Model):
    __tablename__ = "brand"   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)

    products = db.relationship('ProductModel', back_populates='brand')

class LocationModel(db.Model):
    __tablename__ = "location"
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    __table_args__ = (db.UniqueConstraint('latitude', 'longitude'), )

    shop = db.relationship('ShopModel', uselist=False, back_populates='location')

class ReviewModel(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_review = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id'), )

    user = db.relationship('UserModel', back_populates='reviews')
    product = db.relationship('ProductModel', back_populates='reviews')

class WishListModel(db.Model):
    __tablename__ = "wishlist"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id'), )

    user = db.relationship('UserModel', back_populates='wishlists')
    product = db.relationship('ProductModel', back_populates='wishlists')


class ShopLikeModel(db.Model):
    __tablename__ = "shop_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), nullable=False)
    upvoted = db.Column(db.Boolean, nullable=False, default=True)
    downvoted = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'shop_id'), )

    user = db.relationship('UserModel', back_populates='shoplikes')
    shop = db.relationship('ShopModel', back_populates='shoplikes')

class RevokedTokenModel(db.Model):
    __tablename__ = "revoked_tokens"
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)