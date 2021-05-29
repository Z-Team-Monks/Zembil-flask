from flask import request
from flask_restx import Resource, abort
from marshmallow import ValidationError
from zembil import db
from zembil.models import LocationModel
from zembil.schemas import LocationSchema

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)

class Locations(Resource):
    def get(self):
        results = LocationModel.query.all()
        return locations_schema.dump(results)

    def post(self):
        data = request.get_json()
        try:
            args = location_schema.load(data)
        except ValidationError as errors:
            abort(400, message=errors.messages)
        location = LocationModel(
            latitude=args['latitude'], 
            longitude=args['longitude'], 
            description=args['description']
        )
        db.session.add(location)
        db.session.commit()
        return location_schema.dump(location), 201

class Location(Resource):
    def get(self, id):
        result = LocationModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Location Not Found")
        return location_schema.dump(result)