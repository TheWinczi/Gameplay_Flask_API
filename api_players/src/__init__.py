# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Flask REST full
from flask_restful import Api

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Define API object which is imported
# by controllers module
api = Api(app)

from .player.controllers.player_controller import PlayersAPI, PlayersByIdAPI

api.add_resource(PlayersAPI, '/api/players')
api.add_resource(PlayersByIdAPI, '/api/players/<int:id>')

# Build the database
db.create_all()

# Initialize default models objects
from .configuration.initialize_data import initialize_models
initialize_models()
