from flask import Blueprint


bp = Blueprint("main", __name__, template_folder="views")

from microblog.main import routes
