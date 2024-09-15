import pytest
from microblog import create_app, db
from microblog.auth import models as auth_models
from microblog.blog.models import Blog
from microblog.todo.models import Todo


@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///project2.db",
            "WTF_CSRF_ENABLED": False,
        }
    )

    yield app


@pytest.fixture
def client(app):
    with app.app_context():
        return app.test_client()


@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()

        user_one = auth_models.User(
            username="testing",
            email="testing@email.com",
        )
        user_one.set_password("a")
        user_two = auth_models.User(
            username="usertwo",
            email="usertwo@email.com",
        )
        user_two.set_password("a")
        db.session.add(user_one)
        db.session.add(user_two)
        db.session.commit()

        todo_one = Todo(title="Todo title one", is_done=0, user=user_one)
        todo_two = Todo(title="Todo title two", is_done=0, user=user_one)
        todo_three = Todo(title="Todo title three", is_done=0, user=user_two)

        db.session.add(todo_one)
        db.session.add(todo_two)
        db.session.add(todo_three)
        db.session.commit()

        blog_one = Blog(
            title="Blog title one", content="This is the content one.", user=user_one
        )
        blog_two = Blog(
            title="Blog title two", content="This is the content two.", user=user_one
        )
        db.session.add(blog_one)
        db.session.add(blog_two)
        db.session.commit()

        yield

        db.drop_all()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email="testing@email.com", password="a"):
        return self._client.post(
            "/auth/login",
            data={"email": email, "password": password},
            content_type="application/x-www-form-urlencoded",
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
