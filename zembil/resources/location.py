from flask_restful import Resource, fields, marshal_with, reqparse, abort
from zembil import db
from zembil.models import LocationModel
from zembil.schemas import LocationSchema

location_schema = LocationSchema()

location_post_arguments = reqparse.RequestParser()
location_post_arguments.add_argument('longitude', type=str, help='longitude Required', required=True)
location_post_arguments.add_argument('latitude', type=str, help='Latitude Required', required=True)
location_post_arguments.add_argument('description', type=str, help='Latitude Required', required=True)

class Location(Resource):
    def get(self, id):
        result = LocationModel.query.filter_by(id=id).first()
        if not result:
            abort(404, message="Location Not Found")
        return location_schema.dump(result)

    def post(self):
        args = location_post_arguments.parse_args()
        location = LocationModel(
            latitude=args['latitude'], 
            longitude=args['longitude'], 
            description=args['description']
        )
        db.session.add(location)
        db.session.commit()
        return location_schema.dump(location), 201

