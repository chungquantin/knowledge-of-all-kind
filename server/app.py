import os
from flask import Flask

def config_flask_app(app: Flask, test_config):
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    config_flask_app(app, test_config)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app