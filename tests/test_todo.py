import pytest
from todo.db import get_db

@pytest.mark.parametrize('path', (
    '/todos',
    '/todos/create',
    '/todos/delete/1'
))
def test_login_required(client, path):
    response = client.get('/todos')
    assert response.headers["Location"] == "/auth/login"

def test_todo_index(client, auth):
    auth.login()
    response = client.get('/todos')
    assert b"Logout" in response.data
    assert b'test title' in response.data
    assert b'data-item-url="/todos/delete/1"' in response.data
    
def test_create(client, auth, app):
    auth.login()
    assert client.get('/todos').status_code == 200
    
    client.post('/todos', data={'title': 'todo item.'})
    
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM todos').fetchone()[0]
        assert count == 4

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/todos/delete/1')
    assert b'deleted' in response.data
    
    with app.app_context():
        db = get_db()
        todo = db.execute('SELECT * FROM todos WHERE id = 1').fetchone()
        assert todo is None

def test_delete_forbidden(client, auth, app):
    auth.login()
    response = client.post('/todos/delete/2')
    assert b'error' in response.data