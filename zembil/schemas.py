import re
from marshmallow import fields, Schema, validate, validates, ValidationError
from zembil import ma
from zembil.models import *

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password_hash", "email", "role", "phone")
        model = UserModel
    username = fields.String(required=True)
    password_hash = fields.String(required=True, load_only=True, data_key="password")
    email = fields.Email(required=True)
    role = fields.String(required=True, validate=lambda n: n == 'user' or n == 'admin')
    phone = fields.String(required=False)

    @validates("phone")
    def validate_mobile(self, value):
        rule = re.compile(r'^\+(?:[0-9]●?){6,14}[0-9]$')

        if not rule.search(value):
            msg = u"Invalid mobile number."
            raise ValidationError(msg)

    @validates("username")
    def validate_username(self, username):
        if bool(UserModel.query.filter_by(username=username).first()):
            raise ValidationError(
                '"{username}" username already exists, '
                'please use a different username.'.format(username=username)
            )
    

class LocationSchema(ma.Schema):
    class Meta:
        fields = ("id", "longitude", "latitude", "description")
        model = LocationModel
    longitude = fields.Float(required=True, validate=lambda n: n > -180 and n < 180)
    latitude = fields.Float(required=True, validate=lambda n: n > -90 and n < 90)
    description = fields.String(required=True, validate=validate.Length(5))

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = CategoryModel
    name = fields.String(required=True, validate=lambda n: n.isalpha())

class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "category_id", "location_id", "building_name", "phone_number1", 
        "phone_number2", "category", "location", "description")
        model = ShopModel
    category_id = fields.Integer(required=True, data_key="categoryid")
    location_id = fields.Integer(required=True, data_key="locationid")
    building_name = fields.String(required=True, data_key="buildingname")
    phone_number1 = fields.String(required=False, data_key="phonenumber1")
    phone_number2 = fields.String(required=False, data_key="phonenumber2")
    description = fields.String(required=True, validate=validate.Length(5))

    user = ma.Nested(UserSchema)
    category = ma.Nested(CategorySchema)
    location = ma.Nested(LocationSchema)

    @validates("phone_number1")
    @validates("phone_number2")
    def validate_mobile(self, value):
        rule = re.compile(r'^\+(?:[0-9]●?){6,14}[0-9]$')

        if not rule.search(value):
            msg = u"Invalid mobile number."
            raise ValidationError(msg)

class BrandSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = BrandModel
    name = fields.String(required=True, validate=lambda n: n.isalpha())

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "shop", "brand", "name", "date", 
        "description", "category", "price", "condition", "image", 
        "delivery_available", "discount", "product_count")
        model = ProductModel
    name = fields.String(required=True)
    date = fields.DateTime()
    description = fields.String(required=True, validate=validate.Length(5))
    price = fields.Float(required=True, validate=lambda n: n > 0)
    condition = fields.Float(required=True, validate=lambda n: n.isalpha())
    image = fields.String(required=False)
    delivery_available = fields.Boolean(required=False, data_key="deliveryavailable")
    discount = fields.Float(required=False, validate=lambda n: n >= 0)
    product_count = fields.Integer(required=False, validate=lambda n: n >= 0, data_key="productcount")    

    shop = ma.Nested(ShopSchema)
    brand = ma.Nested(BrandSchema)
    category = ma.Nested(CategorySchema)

    @validates("image")
    def validate_url(self, value):
        regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not re.match(regex, value):
            msg = u"Invalid image url."
            raise ValidationError(msg)

class ShopProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "building_name", "phone_number1", 
        "phone_number2", "category", "location", "description", "products")
        model = ShopModel
    user = ma.Nested(UserSchema)
    category = ma.Nested(CategorySchema)
    location = ma.Nested(LocationSchema)
    products = ma.List(ma.Nested(ProductSchema))

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "product", "rating", "review_text", "date")
        model = ReviewModel
    rating = fields.Integer(required=False, validate=lambda n: n > 0 and n < 6)
    review_text = fields.String(required=False, data_key="reviewtext")
    user = ma.Nested(UserSchema)
    product = ma.Nested(ProductSchema)

class ProductReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "date", "building_name", 
        "description", "price", "condition", "image", 
        "delivery_available", "discount", "product_count", "reviews")
        model = ProductModel
    reviews = ma.List(ma.Nested(ReviewSchema()))

class CategoryShopsSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "shops")
        model = CategoryModel
    shops = ma.List(ma.Nested(ShopSchema))

class WishListSchema(ma.Schema):
    class Meta:
        fields = ("id", "product_id", "product", "user", "date")
        model = WishListModel
    product_id = fields.Integer(required=True, load_only=True, )
    product = ma.Nested(ProductSchema)
    user = ma.Nested(UserSchema)

class UserWishListSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "role", "phone", "wishlists")
        model = UserModel
    wishlists = ma.List(ma.Nested(WishListSchema))

class ShopLikeSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "shop")
        model = ShopLikeModel
    user = ma.Nested(UserSchema)
    shop = ma.Nested(ShopSchema)

class TotalShopLikes(ma.Schema):
    class Meta:
        fields = ("id", "user", "shoplikes", "building_name", "phone_number1", 
        "phone_number2", "category", "location", "description")
        model = ShopLikeModel
    user = ma.Nested(UserSchema)
    shoplikes = ma.List(ma.Nested(ShopLikeSchema))

