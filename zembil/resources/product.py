from flask_restful import Resource, fields, reqparse, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import ProductModel, UserModel
from zembil.schemas import ProductSchema
from zembil.common.util import cleanNullTerms


product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

product_post_arguments = reqparse.RequestParser()
product_post_arguments.add_argument("shopid", type=int, help="Shop id is required", required=True)
product_post_arguments.add_argument("brandid", type=int, help="Brand id is required", required=False)
product_post_arguments.add_argument("categoryid", type=int, help="Brand id is required", required=False)
product_post_arguments.add_argument("name", type=str, help="Product name is required", required=True)
product_post_arguments.add_argument("description", type=str, help="Description", required=False)
product_post_arguments.add_argument("price", type=float, help="Price is required", required=True)
product_post_arguments.add_argument("condition", type=str, help="Condition", required=False)
product_post_arguments.add_argument("imageurl", type=str, help="Image", required=False)
product_post_arguments.add_argument("deliveryavailable", type=bool, help="Delivery Available", required=False)
product_post_arguments.add_argument("discount", type=float, help="Discount", required=False)
product_post_arguments.add_argument("productcount", type=int, help="Product Count", required=False)

product_put_arguments = reqparse.RequestParser()
product_put_arguments.add_argument("brandid", type=int, help="Brand id", required=False, location='json')
product_put_arguments.add_argument("categoryid", type=int, help="Brand id", required=False, location='json')
product_put_arguments.add_argument("name", type=str, help="Product name", required=False, location='json')
product_put_arguments.add_argument("description", type=str, help="Description", required=False, location='json')
product_put_arguments.add_argument("price", type=float, help="Price", required=False, location='json')
product_put_arguments.add_argument("condition", type=str, help="Condition", required=False, location='json')
product_put_arguments.add_argument("imageurl", type=str, help="Image", required=False, location='json')
product_put_arguments.add_argument("deliveryavailable", type=bool, help="Delivery Available", required=False, location='json')
product_put_arguments.add_argument("discount", type=float, help="Discount", required=False, location='json')
product_put_arguments.add_argument("productcount", type=int, help="Product Count", required=False, location='json')


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
                image=args["imageurl"],
                delivery_available=args["deliveryavailable"],
                discount=args["discount"],
                product_count=args["productcount"]
            )
            db.session.add(product)
            db.session.commit()
            return product_schema.dump(product), 201
        abort(403, message="Unauthorized access")
        

class Product(Resource):
    def get(self, id):
        product = ProductModel.query.filter_by(id=id).first()
        if product:
            return product_schema.dump(product)
        abort(404, message="Product doesn't exist!") 

    @jwt_required()
    def patch(self, id):
        args = cleanNullTerms(product_put_arguments.parse_args())
        existing = ProductModel.query.get(id)
        if existing and args:
            product = ProductModel.query.filter_by(id=id).update(args)
            db.session.commit()
            return product_schema.dump(ProductModel.query.get(id)), 200
        if not existing:
            abort(404, message="Product doesn't exist!") 
        abort(400, message="Empty body was given")
