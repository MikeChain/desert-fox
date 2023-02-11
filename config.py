import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", default="super secret key")
    REDIS_URI = os.environ.get("REDIS_URI", default="redis://localhost:6379")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get("FLASK_DEBUG", default=False)
    API_TITLE = "Desert fox REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"


class DevConfig(Config):
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https:cdn.jsdelivr.net/npm/swagger-ui-dist/"
    PROPAGATE_EXCEPTIONS = True


class QasConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"{os.environ.get('DATABASE_URI')}_test"


class PrdConfig(Config):
    DEBUG = False


envs: dict[str, Config] = {
    "dev": DevConfig,
    "qas": QasConfig,
    "prd": PrdConfig,
}
