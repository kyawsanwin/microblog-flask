from flask import render_template, request, flash, g

from microblog.auth.decorators import login_required
from werkzeug.exceptions import abort
from microblog.todo import bp
from microblog import db
from microblog.todo.models import Todo
from sqlalchemy import select


def get_todo(id, check_author=True):
    todo = db.session.execute(select(Todo).where(Todo.id == id)).scalar_one_or_none()

    if todo is None:
        abort(404, description=f"Todo id {id} doesn't exist.")

    if check_author and todo.user_id != g.user.id:
        abort(403, description="Not authorized.")
    return todo


@bp.route("", methods=("GET", "POST"))
@login_required
def index():
    if request.method == "POST":
        title = request.form["title"]

        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            todo = Todo(title=title, user_id=g.user.id)
            db.session.add(todo)
            db.session.commit()

    todos = db.session.execute(select(Todo).where(Todo.user_id == g.user.id)).scalars()

    return render_template("todo/index.html", todos=todos)


@bp.route("/delete/<int:id>", methods=("POST",))
@login_required
def delete(id):
    # dba.execute(s.delete(Todo).where(Todo.id == id))
    # todo = dba.session.execute(select(Todo).where(Todo.id == id)).first()
    todo = get_todo(id)
    db.session.delete(todo)
    db.session.commit()
    return {"status": 200, "deleted": 1}


@bp.route("/<int:id>/action", methods=("POST",))
@login_required
def action(id):
    if request.method == "POST":
        is_done = request.form["is_done"]
        todo = get_todo(id)
        todo.is_done = is_done
        db.session.commit()
        return {"status": 200, "updated": 1}


@bp.route("/<int:id>/update", methods=("POST",))
@login_required
def update(id):
    if request.method == "POST":
        title = request.form["title"]
        todo = get_todo(id)
        todo.title = title
        db.session.commit()
        return {"status": 200, "updated": 1}
