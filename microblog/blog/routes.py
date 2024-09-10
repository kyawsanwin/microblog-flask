from microblog.blog import bp


@bp.route("")
def index():
    return "Blog"
