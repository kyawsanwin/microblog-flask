import os
import uuid
from flask import Flask, jsonify


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=str(uuid.uuid4()),
        DATABASE=os.path.join(app.instance_path, "todo.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(error=str(e)), 404

    @app.errorhandler(403)
    def user_forbidden(e):
        return jsonify(error=str(e)), 403

    from .main import bp as main_bp

    app.register_blueprint(main_bp)

    from .blog import bp as blog_bp

    app.register_blueprint(blog_bp)

    from . import db

    db.init_app(app)

    from .auth import bp as auth_bp

    app.register_blueprint(auth_bp)

    from .todo import bp as todo_bp

    app.register_blueprint(todo_bp)
    return app
