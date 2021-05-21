from zembil import ma
from zembil.models import *

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "email", "role", "phone")
        model = UserModel

class LocationSchema(ma.Schema):
    class Meta:
        fields = ("id", "longitude", "latitude", "description")
        model = LocationModel

class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = CategoryModel

class ShopSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "building_name", "phone_number1", 
        "phone_number2", "category", "location", "description")
        model = ShopModel
    user = ma.Nested(UserSchema)
    category = ma.Nested(CategorySchema)
    location = ma.Nested(LocationSchema)

class BrandSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = BrandModel

class ProductSchema(ma.Schema):
    class Meta:
        fields = ("id", "shop", "brand", "name", "date", "building_name", 
        "description", "category", "price", "condition", "image", 
        "delivery_available", "discount", "product_count")
        model = ProductModel
    shop = ma.Nested(ShopSchema)
    brand = ma.Nested(BrandSchema)
    category = ma.Nested(CategorySchema)

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "product", "rating", "user_review", "date")
        model = ReviewModel
    user = ma.Nested(UserSchema)
    product = ma.Nested(ProductSchema)

class WishListSchema(ma.Schema):
    class Meta:
        fields = ("id", "product", "user", "date")
        model = WishListModel
    product = ma.Nested(ProductSchema)
    user = ma.Nested(UserSchema)

class ShopLikeSchema(ma.Schema):
    class Meta:
        fields = ("id", "user", "shop")
        model = ShopLikeModel
    user = ma.Nested(UserSchema)
    shop = ma.Nested(ShopSchema)


