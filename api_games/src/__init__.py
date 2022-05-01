from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

import os


api = None
app = None
db = None


def create_app(test_config=None):
    # create and configure the app
    global app
    app = Flask(__name__,
                instance_path=os.path.abspath(os.path.dirname(__file__)))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('../config.py', silent=True)
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

    from api_games.src.game.controller.game_controller import GamesAPI, GamesByIdAPI, GamesByIdPlayersAPI
    from api_games.src.player.controller.player_controller import PlayersAPI, PlayersByIdAPI
    from api_games.src.playing.controller.playing_controller import GamesByIdPlayersByIdAPI
    api.add_resource(GamesAPI, '/api/games')
    api.add_resource(GamesByIdAPI, '/api/games/<int:game_id>')
    api.add_resource(GamesByIdPlayersAPI, '/api/games/<int:game_id>/players')
    api.add_resource(GamesByIdPlayersByIdAPI, '/api/games/<int:game_id>/players/<int:player_id>')
    api.add_resource(PlayersAPI, '/api/players')
    api.add_resource(PlayersByIdAPI, '/api/players/<int:player_id>')

    # Build the database
    db.create_all()

    if app.config.get("INITIALIZE_MODELS", False):
        from api_games.src.configuration.initialize_data import initialize_models
        initialize_models()

    # Set needed variables for logging if needed
    if app.config.get("ENABLE_LOGGING", False):
        if not app.config.get("API_GAMES_LOGGING_FILE", False):
            app.config["API_GAMES_LOGGING_FILE"] = "instance/api_games_logs.log"

    # Add swagger to url
    if app.config.get("ADD_SWAGGER", False):
        swagger_bp = get_swaggerui_blueprint(
            app.config.get('SWAGGER_URL', '/api/swagger'),
            app.config.get('API_DEFINITION_FILE_URL', '/static/swagger/swagger.json'),
            config=app.config.get("SWAGGER_CONFIG", {})
        )
        app.register_blueprint(swagger_bp)

    from api_games.src.player.event.player_event import PlayerEventsHandler
    events_handler = PlayerEventsHandler()
    events_handler.start()

    return app
