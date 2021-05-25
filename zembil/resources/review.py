from flask_restful import Resource, fields, reqparse, abort
from flask_jwt_extended import ( jwt_required, get_jwt_identity)
from zembil import db
from zembil.models import ReviewModel
from zembil.schemas import ReviewSchema

review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

review_post_arguments = reqparse.RequestParser() # product_id, rating, user_review
review_post_arguments.add_argument('productid', type=int, help="Product id is required", required=True)
review_post_arguments.add_argument('rating', type=float, required=True, help="Rating is required")
review_post_arguments.add_argument('userreview', type=str, required=False)


class Reviews(Resource):
    def get(self):
        reviews = ReviewSchema.query.all()
        if reviews:
            return reviews_schema.dump(reviews)
        return abort(404, "No Reviews found yet!")
    
    @jwt_required()
    def post(self):
        args = review_post_arguments.parse_args()
        user_id = get_jwt_identity()
        existing = ReviewModel.query.filter_by(user_id=user_id, product_id=args['productid']).first()
        if not existing:
            review = ReviewModel(
                product_id=args['productid'],
                user_id=user_id,
                rating=args['rating'],
                user_review=user['userreview']
            )
            db.session.add(review)
            db.session.commit()
            return review_schema.dump(review), 201
        return abort(409, "User already rated this product")


    



