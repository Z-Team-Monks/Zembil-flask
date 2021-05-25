import os 
from datetime import timedelta

class Config:
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    JWT_BLACKLIST_ENABLED = ['access']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(6 * 30)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password1@localhost:5432/zembilflask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False