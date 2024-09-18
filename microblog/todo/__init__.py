from flask import Blueprint


bp = Blueprint("todo", __name__, url_prefix="/todos", template_folder="views")

from microblog.todo import routes
