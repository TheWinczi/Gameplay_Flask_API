import time

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
    time.sleep(10)
    global app
    app = Flask(__name__,
                instance_path=os.path.abspath(os.path.dirname(__file__)),
                static_url_path='/api/accounts/static/',
                static_folder='static')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        if app.config.get('ENV', 'production').lower() == 'production':
            app.config.from_pyfile('../production.config.py', silent=True)
        else:
            app.config.from_pyfile('../development.config.py', silent=True)
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

    from api_accounts.src.account.controller.account_controller import AccountsAPI, AccountsByLoginAPI
    api.add_resource(AccountsAPI, '/api/accounts')
    api.add_resource(AccountsByLoginAPI, '/api/accounts/<login>')

    from api_accounts.src.account.controller.account_controller import AccountsAuthenticationAPI
    api.add_resource(AccountsAuthenticationAPI, '/api/accounts/authentication')

    # Build the database
    db.drop_all()
    db.create_all()

    # Initialize default models objects
    if app.config.get("INITIALIZE_MODELS", False):
        from api_accounts.src.configuration.initialize_data import initialize_models
        initialize_models()

    # Set needed variables for logging if needed
    if app.config.get("ENABLE_LOGGING", False):
        if not app.config.get("API_ACCOUNTS_LOGGING_FILE", False):
            app.config["API_ACCOUNTS_LOGGING_FILE"] = "instance/api_accounts_logs.log"

    # Add swagger to url
    if app.config.get("ADD_SWAGGER", False):
        swagger_bp = get_swaggerui_blueprint(
            app.config.get('SWAGGER_URL', '/api/accounts/swagger'),
            app.config.get('API_DEFINITION_FILE_URL', '/static/swagger/swagger.json'),
            config=app.config.get("SWAGGER_CONFIG", {})
        )
        app.register_blueprint(swagger_bp)

    return app
