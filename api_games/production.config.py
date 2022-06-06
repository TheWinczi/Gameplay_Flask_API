# Statement for enabling the production environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'games.db') # 'sqlite:///:memory:'
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

INITIALIZE_MODELS = False

# Variables responsible for logging
ENABLE_LOGGING = True
API_GAMES_LOGGING_FILE = "instance/api_games_logs.log"

# Secret key for signing cookies
SECRET_KEY = "absolutely_secret_key"

# Swagger configuration
ADD_SWAGGER = True
SWAGGER_URL = '/api/swagger'
API_DEFINITION_FILE_URL = '/static/swagger/swagger.json'
SWAGGER_CONFIG = {
    'app name': 'Games API Swagger'
}
