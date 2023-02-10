from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate

from app.extensions import db

import app.models

BPS_TO_IMPORT = ()
migrate = Migrate()


def create_app(environment):
    app = Flask(__name__)

    app.config.from_object(environment)

    db.init_app(app)

    migrate.init_app(app, db)
    api = Api(app)

    @app.route("/test/")
    def test_page():
        return "<h1>Probando el patrón de fábrica de aplicaciones Flask</h1>"

    for bp in BPS_TO_IMPORT:
        api.register_blueprint(bp)

    return app
