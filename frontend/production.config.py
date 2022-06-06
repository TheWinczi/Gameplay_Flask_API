# Statement for enabling the production environment
DEBUG = False

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

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

# Other services addresses
PLAYERS_SERVER_URL = "http://api_gateway:8000/"
GAMES_SERVER_URL = "http://api_gateway:8000/"
ACCOUNTS_SERVER_URL = "http://api_gateway:8000/"

MAX_CONTENT_SIZE = 200 * 200
PLAYER_IMAGE_FILE_ALLOWED_EXTENSIONS = (".png", ".jpeg", ".jpg", ".bmp")
