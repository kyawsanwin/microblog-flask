from flask import g, redirect, render_template, request, url_for
from sqlalchemy import select
from microblog.auth.decorators import login_required
from microblog.blog import bp
from microblog import db
from microblog.blog.forms import BlogForm
from microblog.blog.models import Blog


@bp.route("")
def index():
    # blogs = db.session.execute(select(Blog)).scalars()
    blogs = db.paginate(select(Blog).order_by(Blog.created_at), per_page=10)
    return render_template("blog/index.html", blogs=blogs)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    form = BlogForm()
    if request.method == "POST" and form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        blog = Blog(title=title, content=content, user_id=g.user.id)
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for("blog.index"))

    return render_template("blog/create.html", form=form)
