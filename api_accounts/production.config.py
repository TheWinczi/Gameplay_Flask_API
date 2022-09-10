# Statement for enabling the production environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
DATABASE_USER_LOGIN = 'root'
DATABASE_USER_PASSWORD = 'root'
DATABASE_ADDRESS = 'mariadb'
DATABASE_TABLE = 'accounts_db'
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

# Secret key for signing cookies
SECRET_KEY = "absolutely_secret_key"

INITIALIZE_MODELS = True

# Variables responsible for logging
ENABLE_LOGGING = True
API_ACCOUNTS_LOGGING_FILE = "instance/api_accounts_logs.log"

# Swagger configuration
ADD_SWAGGER = True
SWAGGER_URL = '/api/accounts/swagger/'
API_DEFINITION_FILE_URL = '/api/accounts/static/swagger/swagger.json'
SWAGGER_CONFIG = {
    'app name': 'Accounts API Swagger'
}
