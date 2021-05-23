from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import db
from zembil.models import CategoryModel
from zembil.schemas import CategorySchema

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

category_post_arguments = reqparse.RequestParser()
category_post_arguments.add_argument('name', type=str, help="Name required", required=True)


class Categories(Resource):
    def get(self):
        result = CategoryModel.query.all()
        return categories_schema.dump(result)
    
    def post(self):
        args = category_post_arguments.parse_args()
        category = CategoryModel(name=args['name'])
        db.session.add(category)
        db.session.commit()
        return category_schema.dump(category), 201

class Category(Resource):
    def get(self, id):
        result = CategoryModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Category Not Found")
        return category_schema.dump(result)