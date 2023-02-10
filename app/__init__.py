from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from config import Config
from app.extensions import db

BPS_TO_IMPORT = ()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate = Migrate(app, db)
    api = Api(app)

    @app.route("/test/")
    def test_page():
        return "<h1>Probando el patrón de fábrica de aplicaciones Flask</h1>"

    for bp in BPS_TO_IMPORT:
        api.register_blueprint(bp)

    return app
