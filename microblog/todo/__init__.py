from flask import Blueprint


bp = Blueprint("todo", __name__, url_prefix="/todos")

from microblog.todo import routes
