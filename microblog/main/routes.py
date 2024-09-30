from microblog.blog.models import Blog
from microblog.main import bp
from flask import g, render_template, session

from microblog.todo.models import Todo


@bp.route("/")
def index():
    posts = Blog().get_latest_posts(limit=5)
    user_id = session.get("user_id")
    todos = None
    if user_id is not None:
        todos = Todo().get_undone_todos(g.user.id)
    return render_template("main/index.html", posts=posts, todos=todos)
