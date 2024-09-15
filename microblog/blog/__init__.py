from flask import Blueprint

bp = Blueprint("blog", __name__, url_prefix="/blog", template_folder="views")

from microblog.blog import routes
