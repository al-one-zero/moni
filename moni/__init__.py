import os, functools

from flask import Flask, redirect, render_template, g, url_for

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)

    # Config init
    app.config.from_mapping(
        SECRET_KEY = 'dev', # TODO Need to change before deployement
        DATABASE = os.path.join(app.instance_path, 'db.sqlite'),
        )
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else :
        app.config.from_mapping(test_config)

    # Instance path folder init
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database init
    from . import db
    db.init_app(app)

    # Blueprints registering
    from . import home, auth, user
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)

    return app

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
