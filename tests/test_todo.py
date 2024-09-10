import pytest
from microblog.db import get_db


def test_login_required(client):
    response = client.get("/todos")
    assert response.headers["Location"] == "/auth/login"


def test_todo_index(client, auth):
    auth.login()
    response = client.get("/todos")
    assert b"Logout" in response.data
    assert b"test title" in response.data
    assert b'data-item-url="/todos/delete/1"' in response.data


def test_create(client, auth, app):
    auth.login()
    assert client.get("/todos").status_code == 200

    client.post("/todos", data={"title": "todo item."})

    with app.app_context():
        db = get_db()
        count = db.execute("SELECT COUNT(id) FROM todos").fetchone()[0]
        assert count == 4


def test_delete(client, auth, app):
    auth.login()
    response = client.post("/todos/delete/1")
    assert b"deleted" in response.data

    with app.app_context():
        db = get_db()
        todo = db.execute("SELECT * FROM todos WHERE id = 1").fetchone()
        assert todo is None


def test_delete_forbidden(client, auth, app):
    auth.login()
    response = client.post("/todos/delete/2")
    assert b"error" in response.data


@pytest.mark.parametrize(
    ("id", "is_done"),
    (
        (1, 1),
        (3, 0),
    ),
)
def test_action(client, auth, app, id, is_done):
    auth.login()
    response = client.post(f"/todos/{id}/action", data={"is_done": is_done})
    assert b"updated" in response.data

    with app.app_context():
        db = get_db()
        todo = db.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        assert todo["is_done"] == is_done


@pytest.mark.parametrize(
    ("id", "title"),
    (
        (1, "Updated one."),
        (3, "Updated two."),
    ),
)
def test_update(client, auth, app, id, title):
    auth.login()
    response = client.post(f"/todos/{id}/update", data={"title": title})
    assert b"updated" in response.data

    with app.app_context():
        db = get_db()
        todo = db.execute("SELECT * FROM todos WHERE id = ?", (id,)).fetchone()
        assert todo["title"] == title
