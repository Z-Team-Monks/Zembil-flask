from flask_restful import Resource

class Shop(Resource):
    def get(self):
        return {'hello': 'world'}
    def put(self):
        pass

class Shops(Resource):
    def get(self):
        return {'hello': 'world'}