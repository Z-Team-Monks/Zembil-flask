from flask_restful import Resource, fields, reqparse, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import ProductModel, UserModel
from zembil.schemas import ProductSchema

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

product_post_arguments = reqparse.RequestParser()
product_post_arguments.add_argument("Authorization", type=str, help="Token is required", required=True)
product_post_arguments.add_argument("shopid", type=int, help="Shop id is required", required=True)
product_post_arguments.add_argument("brandid", type=int, help="Brand id is required", required=True)
product_post_arguments.add_argument("categoryid", type=int, help="Brand id is required", required=True)
product_post_arguments.add_argument("name", type=str, help="Product name is required", required=True)
product_post_arguments.add_argument("description", type=str, help="Description", required=False)
product_post_arguments.add_argument("price", type=float, help="Price is required", required=True)
product_post_arguments.add_argument("condition", type=str, help="Condition", required=False)
product_post_arguments.add_argument("image", type=str, help="Image", required=False)
product_post_arguments.add_argument("deliveryavailable", type=bool, help="Delivery Available", required=False)
product_post_arguments.add_argument("discount", type=float, help="Discount", required=False)
product_post_arguments.add_argument("productcount", type=int, help="Product Count", required=False)


class Products(Resource):
    def get(self):
        products = ProductModel.query.all()
        return products_schema.dump(products)
    
    @jwt_required()
    def post(self):
        args = product_post_arguments.parse_args()
        user_id = get_jwt_identity()
        shop_owner = UserModel.query.filter_by(id=user_id).first()
        if shop_owner:
            product = ProductModel(
                shop_id=args["shopid"],
                brand_id=args["brandid"],
                category_id=args["categoryid"],
                name=args["name"],
                description=args["description"],
                price=args["price"],
                condition=args["condition"],
                image=args["image"],
                delivery_available=args["deliveryavailable"],
                discount=args["discount"],
                product_count=args["productcount"]
            )
            db.session.add(product)
            db.session.commit()
            return product_schema.dump(product), 
        else:
            abort(403, message="Unauthorized access")
        

class Product(Resource):
    def get(self, id):
        product = ProductModel.query.filter_by(id=id).first()
        return product_schema.dump(product)