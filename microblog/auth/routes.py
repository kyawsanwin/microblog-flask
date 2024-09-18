from flask import (
    render_template,
    request,
    redirect,
    flash,
    url_for,
    session,
    g,
)
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash
from microblog.auth.decorators import check_already_loggedin
from microblog.auth.forms import RegistrationForm, LoginForm
from microblog.auth.models import User
from microblog import db
from microblog.auth import bp
from sqlalchemy.exc import IntegrityError, NoResultFound


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = db.session.execute(select(User).filter_by(id=user_id)).scalar_one()


@bp.route("/login", methods=("GET", "POST"))
@check_already_loggedin
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        error = None
        user = None
        try:
            user = db.session.execute(select(User).filter_by(email=email)).scalar_one()
            if not user.check_password(password):
                error = "Incorrect password."
        except NoResultFound:
            error = "Incorrect email address."

        if error is None:
            session.clear()
            session["user_id"] = user.id

            return redirect(url_for("todo.index"))

        flash(error)
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=("GET", "POST"))
@check_already_loggedin
def register():
    form = RegistrationForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User(
            username=username, email=email, password=generate_password_hash(password)
        )
        error = None
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            error = f"{username} or {email} is already registered."
        else:
            return redirect(url_for("auth.login"))

        flash(error)
    return render_template("auth/register.html", form=form)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
