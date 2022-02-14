from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

import os


api = None
app = None
db = None


def create_app(test_config=None):
    # create and configure the app
    global app
    app = Flask(__name__,
                instance_relative_config=True,
                instance_path=os.path.abspath(os.path.dirname(__file__)))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    global db
    db = SQLAlchemy(app)

    global api
    api = Api(app)

    from api_players.src.player.controller.player_controller import PlayersAPI, PlayersByIdAPI
    api.add_resource(PlayersAPI, '/api/players')
    api.add_resource(PlayersByIdAPI, '/api/players/<int:id>')

    # Build the database
    db.drop_all()
    db.create_all()

    # Initialize default models objects
    if app.config.get("INITIALIZE_MODELS", False):
        from api_players.src.configuration.initialize_data import initialize_models
        initialize_models()

    return app
