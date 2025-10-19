from flask import Flask
from flask_cors import CORS


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object('api.config.Config')

    CORS(app)

    return app