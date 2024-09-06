import functools

from flask import(
    Blueprint, render_template, request, redirect, flash, url_for, session, g
)
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

def check_already_loggedin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user:
            return redirect(url_for('todo.index'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/login', methods=('GET', 'POST'))
@check_already_loggedin
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        db = get_db()
        
        error = None
        
        user = db.execute(
            'SELECT * FROM users WHERE email = ?', (email,)
        ).fetchone()
        
        if user is None:
            error = 'Incorrect email address.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.route('/register', methods=('GET', 'POST'))
@check_already_loggedin
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        db = get_db()
        
        error = None
        
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required'
        elif not confirm_password:
            error = 'Confirm password is required'
        elif password != confirm_password:
            error = "Confirm password doesn't match."
        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                    (username, email, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"{username} or {email} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
        
    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view