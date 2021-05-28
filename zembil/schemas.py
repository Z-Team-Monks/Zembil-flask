import re
from marshmallow import fields, Schema, validate, validates, ValidationError
from zembil import ma
from zembil.models import *

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "username", "password_hash", "email", "date", "role", "phone")
        model = UserModel
        ordered = True
    name = fields.String(required=False)
    username = fields.String(required=True)
    password_hash = fields.String(required=True, load_only=True, data_key="password")
    email = fields.Email(required=True)
    role = fields.String(load_only=True)
    phone = fields.String(required=False)
    date = fields.DateTime(dump_only=True, data_key="registration_key")

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
        ordered = True
    longitude = fields.Float(required=True, validate=lambda n: n > -180 and n < 180)
    latitude = fields.Float(required=True, validate=lambda n: n > -90 and n < 90)
    description = fields.String(required=True, validate=validate.Length(5))

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = CategoryModel
        ordered = True
    name = fields.String(required=True, validate=lambda n: n.isalpha())

class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "user_id", "location", "category_id", "building_name", "phone_number1", 
        "phone_number2", "category", "description")
        model = ShopModel
        ordered = True
    name = fields.String(required=False)
    user_id = fields.Integer(data_key="userid")
    category_id = fields.Integer(required=True, data_key="categoryid")
    category = fields.Pluck(CategorySchema, "name", dump_only=True)
    building_name = fields.String(required=True, data_key="buildingname")
    phone_number1 = fields.String(required=False, data_key="phonenumber1")
    phone_number2 = fields.String(required=False, data_key="phonenumber2")
    description = fields.String(required=True, validate=validate.Length(5))

    location = ma.Nested(LocationSchema)

    @validates("phone_number1")
    @validates("phone_number2")
    def validate_mobile(self, value):
        rule = re.compile(r'^\+(?:[0-9]●?){6,14}[0-9]$')

        if not rule.search(value):
            msg = u"Invalid mobile number."
            raise ValidationError(msg)

class RatingSchema(ma.Schema):
    class Meta:
        fields = ("ratingcount", "totalrating")
        ordered = True
    totalrating = fields.Float(dump_only=True)
    ratingcount = fields.Integer(dump_only=True)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "shop_id", "brand", "name", "date", 
        "description", "category", "category_id", "price", "condition", "image", 
        "delivery_available", "discount", "product_count")
        model = ProductModel
        ordered = True
    id = fields.Integer()
    name = fields.String(required=True)
    date = fields.DateTime(dump_only=True)
    brand = fields.String(required=False, data_key="brand")
    shop_id = fields.Integer(required=True, data_key="shopid")
    category_id = fields.Integer(required=True, data_key="categoryid", load_only=True)
    category = fields.Pluck(CategorySchema, 'name', dump_only=True)
    description = fields.String(required=True, validate=validate.Length(5))
    price = fields.Float(required=True, validate=lambda n: n > 0)
    condition = fields.String(required=True, validate=lambda n: n.isalpha())
    image = fields.String(required=False, data_key="imageurl")
    delivery_available = fields.Boolean(required=False, data_key="deliveryavailable")
    discount = fields.Float(required=False, validate=lambda n: n >= 0)
    product_count = fields.Integer(required=False, validate=lambda n: n >= 0, data_key="productcount")

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
        fields = ("id", "products")
        model = ShopModel
        ordered = True
    id = fields.Integer(data_key="shopid")
    products = ma.List(ma.Nested(ProductSchema))


class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "product_id", "rating", "review_text", "date")
        model = ReviewModel
        ordered = True
    rating = fields.Integer(required=False, validate=lambda n: n > 0 and n < 6)
    review_text = fields.String(required=False, data_key="reviewtext")
    user = ma.Nested(UserSchema)
    product_id = fields.Integer(dump_only=True, data_key="productid")

class ProductReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "reviews")
        model = ProductModel
        ordered = True
    id = fields.Integer(data_key="productid")
    reviews = ma.Nested(ReviewSchema(many=True))

class CategoryShopsSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "shops")
        model = CategoryModel
        ordered = True
    shops = ma.Nested(ShopSchema(many=True))

class WishListSchema(ma.Schema):
    class Meta:
        fields = ("id", "product_id", "user_id", "date")
        model = WishListModel
        ordered = True
    user_id = fields.Integer(data_key="userid")
    product_id = fields.Integer(required=True, data_key="productid")

class UserWishListSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "role", "phone", "wishlists")
        model = UserModel
        ordered = True
    wishlists = ma.List(ma.Nested(WishListSchema))

class ShopLikeSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "shop_id")
        model = ShopLikeModel
        ordered = True
    user_id = fields.Integer(data_key="userid")
    shop_id = fields.Integer(data_key="shopid")

class TotalShopLikeSchema(ma.Schema):
    class Meta:
        fields = ("id", "building_name", "phone_number1", "phone_number2",
         "description", "shoplikes")
        model = ShopModel
        ordered = True
    id = fields.Integer(data_key="shopid")
    user = ma.Nested(UserSchema)
    shoplikes = ma.List(ma.Nested(ShopLikeSchema))

