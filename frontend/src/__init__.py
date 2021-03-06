from flask import Flask, render_template

import os

app = None


def create_app(test_config=None):
    # create and configure the app
    global app
    app = Flask(__name__,
                instance_path=os.path.abspath(os.path.dirname(__file__)))

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

    import frontend.src.gameplay.views
    import frontend.src.errors.views

    return app
