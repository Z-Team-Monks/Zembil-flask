from flask import request, current_app, jsonify
from flask_restful import Resource, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from marshmallow import ValidationError
from sqlalchemy import func
from werkzeug.utils import secure_filename
from zembil import db
from zembil.models import ProductModel, ShopModel, CategoryModel, ReviewModel
from zembil.schemas import ProductSchema, ShopProductSchema, RatingSchema
from zembil.common.util import clean_null_terms
from zembil.common.helper import PaginationHelper

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

shop_products_schema = ShopProductSchema()

class Products(Resource):
    def get(self):
        limit = request.args.get('limit')
        results_per_page = current_app.config['PAGINATION_PAGE_SIZE']
        if limit:
            results_per_page = int(limit)
        pagination_helper = PaginationHelper(
            request,
            query=ProductModel.query,
            resource_for_url='api_v1.products',
            key_name='results',
            schema=products_schema,
            results_per_page=results_per_page
        )
        result = pagination_helper.paginate_query()
        return result
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            image = request.files['file']
            if image and image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FILE'], filename))
                data['image'] = filename
        except:
            pass
        try:
            args = product_schema.load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        args = clean_null_terms(args)
        user_id = get_jwt_identity()
        shop_owner = ShopModel.query.filter_by(user_id=user_id).first()
        if shop_owner and args:
            product = ProductModel(**args)
            db.session.add(product)
            db.session.commit()
            return product_schema.dump(product), 201
        abort(403, message="Shop doesn't belong to this user")

class Product(Resource):
    def get(self, id):
        product = ProductModel.query.get(id)
        if product:
            average_rating = ReviewModel.query.with_entities(
                                    func.avg(ReviewModel.rating).label("sum")
                        ).filter_by(product_id=id).first()[0]
            ratingcount = ReviewModel.query.filter_by(product_id=id).count()
            data = product_schema.dump(product)
            if not average_rating:
                average_rating = 0.0
            rating = RatingSchema().dump({
                'averageRating': average_rating,
                'ratingcount': ratingcount
            })
            return jsonify({"product": data, "rating": rating})
        abort(404, message="Product doesn't exist!") 

    @jwt_required()
    def patch(self, id):
        data = request.get_json()
        image = request.files['file']
        if image and image.filename == '':
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FILE'], filename))
            data['image'] = filename
        try:
            args = ProductSchema(partial=True).load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        args = clean_null_terms(args)
        existing = ProductModel.query.get(id)
        if existing and args:
            product = ProductModel.query.filter_by(id=id).update(args)
            db.session.commit()
            return product_schema.dump(product), 200
        if not existing:
            abort(404, message="Product doesn't exist!")
        abort(400, message="Empty body was given")

class ShopProducts(Resource):
    def get(self, shop_id):
        shop = ShopModel.query.get(shop_id)
        if shop:
            return shop_products_schema.dump(shop)
        abort(404, message="Shop doesn't exist!")


class SearchProduct(Resource):
    def get(self):
        name = request.args.get('name')
        category = request.args.get('category')
        products = ProductModel.query
        if name:
            products = products.filter(ProductModel.name.ilike('%' + name + '%'))
        if category:
            products = products.filter(CategoryModel.name.ilike('%' + category + '%'))
        products = products.order_by(ProductModel.name).all()
        if products:
            return products_schema.dump(products)
        abort(404, message="Product doesn't exist!")

class FilterProduct(Resource):
    def get(self):
        min_price = request.args.get('minPrice')
        max_price = request.args.get('maxPrice')
        products = ProductModel.query
        if min_price:
            products = products.filter(ProductModel.price >= float(min_price))
        if max_price:
            products = products.filter(ProductModel.price <= float(max_price))
        if products:
            return products_schema.dump(products)
        abort(404, message="Product doesn't exist!")


class TrendingProduct(Resource):
    def get(self):
        s = request.args.get('s')
        products = ProductModel.query
        if s:
            if s == 'latest':
                products = products.order_by(ProductModel.date.desc())
            if s == 'popular':
                sub_query = db.session.query(
                    ReviewModel.product_id, 
                    func.avg(ReviewModel.rating).label('rating')
                    ).group_by(ReviewModel.product_id).subquery()
                products = db.session.query(
                        ProductModel).join(
                    sub_query, 
                    ProductModel.id == sub_query.c.product_id
                    ).order_by(sub_query.c.rating.desc())
            results_per_page = current_app.config['PAGINATION_PAGE_SIZE']
            pagination_helper = PaginationHelper(
                request,
                query=products,
                resource_for_url='api_v1.trendingproduct',
                key_name='results',
                schema=products_schema,
                results_per_page=results_per_page
            )
            result = pagination_helper.paginate_query()
            return result
        abort(404, message="Product doesn't exist")

