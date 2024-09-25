import uuid
from microblog import create_app


def test_config():
    assert not create_app().testing
    assert create_app(
        {
            "SECRET_KEY": str(uuid.uuid4()),
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///project2.db",
            "WTF_CSRF_ENABLED": False,
        }
    ).testing


def test_home(client):
    response = client.get("/")
    assert b"Home" in response.data
