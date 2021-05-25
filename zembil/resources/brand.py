from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import db
from zembil.models import BrandModel
from zembil.schemas import BrandSchema

brand_schema = BrandSchema()
brands_schema = BrandSchema(many=True)

brand_post_arguments = reqparse.RequestParser()
brand_post_arguments.add_argument('name', type=str, help="Name required", required=True)


class Brands(Resource):
    def get(self):
        result = BrandModel.query.all()
        return brands_schema.dump(result)
    
    def post(self):
        args = brand_post_arguments.parse_args()
        brand = BrandModel(name=args['name'])
        db.session.add(brand)
        db.session.commit()
        return brand_schema.dump(brand), 201

class Brand(Resource):
    def get(self, id):
        result = BrandModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Brand Not Found")
        return brand_schema.dump(result)