import pytest
from sqlalchemy import select
from microblog import db
from microblog.todo.models import Todo


def test_login_required(client):
    response = client.get("/todos")
    assert response.headers["Location"] == "/auth/login"


def test_todo_index(client, auth, init_db):
    auth.login()
    response = client.get("/todos")
    assert b"Logout" in response.data
    assert b"Todo title one" in response.data
    assert b'data-item-url="/todos/delete/1"' in response.data


def test_create(client, auth, app, init_db):
    auth.login()
    assert client.get("/todos").status_code == 200

    client.post("/todos", data={"title": "todo item."})

    with app.app_context():
        # count = dba.select([dba.func.count()]).select_from(Todo).scalar()
        count = db.session.query(Todo).count()
        assert count == 4


def test_delete(client, auth, app, init_db):
    auth.login()
    response = client.post("/todos/delete/1")
    assert b"deleted" in response.data

    with app.app_context():
        # todo = dba.session.get(Todo, 1)
        todo = db.session.execute(select(Todo).where(Todo.id == 1)).first()
        assert todo is None


def test_delete_forbidden(client, auth, app, init_db):
    auth.login()
    response = client.post("/todos/delete/3")
    assert b"error" in response.data


@pytest.mark.parametrize(
    ("id", "is_done"),
    (
        (1, 1),
        (2, 0),
    ),
)
def test_action(client, auth, app, id, is_done, init_db):
    auth.login()
    response = client.post(f"/todos/{id}/action", data={"is_done": is_done})
    assert b"updated" in response.data

    with app.app_context():
        todo = db.session.execute(select(Todo).where(Todo.id == id)).scalar_one()
        assert todo.is_done == is_done


@pytest.mark.parametrize(
    ("id", "title"),
    (
        (1, "Updated one."),
        (2, "Updated two."),
    ),
)
def test_update(client, auth, app, id, title, init_db):
    auth.login()
    response = client.post(f"/todos/{id}/update", data={"title": title})
    assert b"updated" in response.data

    with app.app_context():
        todo = db.session.execute(select(Todo).where(Todo.id == id)).scalar_one()
        assert todo.title == title
