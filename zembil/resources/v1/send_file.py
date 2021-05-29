from flask import send_from_directory
from flask_restful import Resource, abort

class SendFile(Resource):
    def get(self, filename):
        try:
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        except FileNotFoundError:
            abort(404, message="File not found!")
