import os

basedir = basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'random ass shit'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or ''
