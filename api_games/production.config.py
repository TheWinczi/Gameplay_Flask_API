# Statement for enabling the production environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the MariaDB database
DATABASE_USER_LOGIN = 'root'
DATABASE_USER_PASSWORD = 'root'
DATABASE_ADDRESS = 'mariadb'
DATABASE_TABLE = 'games_db'
DATABASE_DRIVER = 'mysql'
SQLALCHEMY_DATABASE_URI = f'{DATABASE_DRIVER}://{DATABASE_USER_LOGIN}:{DATABASE_USER_PASSWORD}@{DATABASE_ADDRESS}:3306/{DATABASE_TABLE}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_CONNECT_OPTIONS = {}
# SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

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
SWAGGER_URL = '/api/games/swagger/'
API_DEFINITION_FILE_URL = '/api/games/static/swagger/swagger.json'
SWAGGER_CONFIG = {
    'app name': 'Games API Swagger'
}

# RabbitMQ connection parameters
RABBITMQ_USER_LOGIN = 'guest'
RABBITMQ_USER_PASSWORD = 'guest'
RABBITMQ_ADDRESS = 'rabbitmq'
RABBITMQ_URL = f'amqp://{RABBITMQ_USER_LOGIN}:{RABBITMQ_USER_PASSWORD}@{RABBITMQ_ADDRESS}/%2f'
