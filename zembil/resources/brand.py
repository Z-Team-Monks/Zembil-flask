from flask import request
from flask_restful import Resource, abort
from marshmallow import ValidationError
from zembil import db
from zembil.models import BrandModel
from zembil.schemas import BrandSchema

brand_schema = BrandSchema()
brands_schema = BrandSchema(many=True)

class Brands(Resource):
    def get(self):
        result = BrandModel.query.all()
        return brands_schema.dump(result)
    
    def post(self):
        data = request.get_json()
        try:
            args = brand_schema.load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
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