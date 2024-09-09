from flask import (
    Blueprint, render_template, request, flash, g, jsonify
)

from todo.auth import login_required
from todo.db import get_db
from werkzeug.exceptions import abort

bp = Blueprint('todo', __name__, url_prefix='/todos')

def get_todo(id, check_author=True):
    todo = get_db().execute(
        'SELECT t.id, title, is_done, user_id FROM todos t'
        ' JOIN users u ON t.user_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()
    
    if todo is None:
        abort(404, description=f"Todo id {id} doesn't exist.")

    if check_author and todo['user_id'] != g.user['id']:
        abort(403, description='Not authorized.')
    return todo

@bp.route('', methods=('GET', 'POST'))
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

@bp.route("/delete/<int:id>", methods=('POST',))
@login_required
def delete(id):
    get_todo(id)
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ?', (id,))
    db.commit()
    return {
        "status": 200,
        "deleted": 1
    }

@bp.route("/<int:id>/action", methods=('POST',))
@login_required
def action(id):
    if request.method == 'POST':
        is_done = request.form['is_done']
        get_todo(id)
        db = get_db()
        db.execute('UPDATE todos SET is_done = ? WHERE id = ?', (is_done, id,))
        db.commit()
        return {
            "status": 200,
            "updated": 1
        }

@bp.route("/<int:id>/update", methods=('POST',))
@login_required
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        get_todo(id)
        db = get_db()
        db.execute('UPDATE todos SET title = ? WHERE id = ?', (title, id,))
        db.commit()
        return {
            "status": 200,
            "updated": 1
        }