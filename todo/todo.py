from flask import (
    Blueprint, render_template, request, flash, g
)

from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__, url_prefix='/todos')

@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():
    if request.method == 'POST':
        title = request.form['title']
        
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO todos (title, user_id)'
                ' VALUES (?, ?)',
                (title, g.user['id'])
            )
            db.commit()

    db = get_db()
    todos = db.execute(
        'SELECT t.id, title, is_done FROM todos t'
        ' JOIN users u ON t.user_id = u.id'
        ' ORDER BY is_done ASC'
    ).fetchall()
    return render_template('todo/index.html', todos=todos)  