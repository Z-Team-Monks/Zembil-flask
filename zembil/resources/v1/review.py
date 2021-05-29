from flask import request
from flask_restx import Resource, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from marshmallow import ValidationError
from zembil import db
from zembil.models import ReviewModel, ProductModel
from zembil.schemas import ReviewSchema, ProductReviewSchema
from zembil.common.util import cleanNullTerms

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)
product_reviews_schema = ProductReviewSchema()

class Reviews(Resource):
    def get(self, product_id):
        product = ProductModel.query.filter_by(id=product_id).first()
        if product:
            return product_reviews_schema.dump(product)
        return abort(404, message="No one reviewed yet!")
    
    @jwt_required()
    def post(self, product_id):
        data = request.get_json()
        try:
            args = review_schema.load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        args = cleanNullTerms(args)
        user_id = get_jwt_identity()
        existing = ReviewModel.query.filter_by(user_id=user_id, product_id=product_id).first()
        if not existing and args:
            review = ReviewModel(
                product_id=product_id,
                user_id=user_id,
                **args
            )
            db.session.add(review)
            db.session.commit()
            return review_schema.dump(review), 201
        return abort(409, message="User already rated this product")

class Review(Resource):
    def get(self, product_id, id):
        review = ReviewModel.query.filter_by(id=id).first()
        if review:
            return review_schema.dump(review)
        return abort(404, message="Review doesn't exist!")

    def delete(self, product_id, id):
        review = ReviewModel.query.get(id)
        if review:
            db.session.delete(review)
            db.session.commit()
            return {"message": "Successfull"}, 204
        return abort(404, message="Review doesn't exist!")

