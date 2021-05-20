from flask_restful import Resource

class Product(Resource):
    def get(self):
        return {'hello': 'world'}

class Products(Resource):
    def get(self):
        return {'hello': 'world'}