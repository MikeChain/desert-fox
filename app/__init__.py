import redis
from flask import Flask
from flask_smorest import Api

import app.models
from app.extensions import db, migrate
from app.routes import BPS_TO_IMPORT


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(environment)

    db.init_app(app)

    migrate.init_app(app, db)
    api = Api(app)

    redis_client = redis.from_url(app.config["REDIS_URI"])

    from .jwt_callbacks import init_jwt

    init_jwt(app, redis_client)

    @app.route("/test")
    def test_page():
        return "<h1>Probando el patrón de fábrica de aplicaciones Flask</h1>"

    @app.route("/")
    def index():
        return "<h1>Bienvenido</h1>"

    for bp in BPS_TO_IMPORT:
        api.register_blueprint(bp)

    return app
