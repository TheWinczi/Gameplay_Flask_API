# Statement for enabling the production environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'players.db') # 'sqlite:///:memory:'
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "absolutely_secret_csrf_key"

# Secret key for signing cookies
SECRET_KEY = "absolutely_secret_key"

INITIALIZE_MODELS = False

# Variables responsible for logging
ENABLE_LOGGING = True
API_PLAYERS_LOGGING_FILE = "instance/api_players_logs.log"

# # Other services addresses
# GAME_SERVER_URL = "http://127.0.0.1:8082/"

# Directory path for storing players images
PLAYERS_IMAGES_DIR = os.path.join(BASE_DIR, "src", "static")

# Swagger configuration
ADD_SWAGGER = True
SWAGGER_URL = '/api/players/swagger/'
API_DEFINITION_FILE_URL = '/api/players/static/swagger/swagger.json'
SWAGGER_CONFIG = {
    'app name': 'Players API Swagger'
}
