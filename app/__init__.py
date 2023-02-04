from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    @app.route('/test/')
    def test_page():
        return '<h1>Probando el patrón de fábrica de aplicaciones Flask</h1>'

    return app