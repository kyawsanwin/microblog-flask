from flask import (
    Blueprint, render_template
)

from todo.auth import login_required

bp = Blueprint('todo', __name__)

@bp.route('/todos')
@login_required
def index():
    return render_template('todo/index.html')