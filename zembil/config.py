import os


class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_BLACKLIST_ENABLED = ['access']
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:niko1122@localhost:5432/zembilflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './zembil/static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    CORS_HEADERS = 'Content-Type'
    PAGINATION_PAGE_SIZE = 5
    PAGINATION_PAGE_ARGUMENT_NAME = 'page'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
