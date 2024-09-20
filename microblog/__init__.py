import os
import uuid
from flask import Flask, jsonify, render_template, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object("microblog.config")
        app.config.from_envvar("MICROBLOG_SETTINGS", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from microblog.auth import models as auth_models
        from microblog.todo import models as todo_models

        db.create_all()

    @app.errorhandler(404)
    def resource_not_found(e):
        return render_template("404.html"), 404

    @app.errorhandler(403)
    def user_forbidden(e):
        return jsonify(error=str(e)), 403

    from .main import bp as main_bp

    app.register_blueprint(main_bp)

    from .blog import bp as blog_bp

    app.register_blueprint(blog_bp)

    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from .todo import bp as todo_bp

    app.register_blueprint(todo_bp)
    return app
