from microblog.main import bp


@bp.route("/")
def index():
    return "Home Page"
