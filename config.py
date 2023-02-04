import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', default="super secret key")
    REDIS_URI = os.environ.get('REDIS_URI', default='redis://localhost:6379')
    SQLALCHEMY_DATABASE_URI  = os.environ.get('DATABASE_URI', default=f'sqlite:///{os.path.join(basedir, "app.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get("FLASK_DEBUG", default=False)
