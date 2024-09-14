import pytest
from flask import g, session
from microblog.auth.models import User
from microblog import db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register",
        data={
            "username": "test1",
            "email": "test1@email.com",
            "password": "a",
            "confirm_password": "a",
        },
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert (
            db.session.execute(db.select(User).filter_by(username="test1")).scalar_one()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "email", "password", "confirm_password", "message"),
    (
        ("", "", "", "", b"Username is required."),
        ("a", "", "", "", b"Email is required."),
        ("a", "a@email.com", "", "", b"Password is required."),
        ("a", "a@email.com", "a", "", b"Confirm password is required."),
        ("a", "a@email.com", "a", "b", b"Confirm password doesn&#39;t match."),
        ("testing", "testing@email.com", "a", "a", b"already registered."),
    ),
)
def test_register_validate_input(
    client, username, email, password, confirm_password, message, init_db
):
    response = client.post(
        "/auth/register",
        data={
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
        },
    )
    assert message in response.data


def test_login(client, auth, init_db):
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    print(response.headers)
    assert response.headers["Location"] == "/todos"

    with client:
        client.get("/todos")
        assert session["user_id"] == 1
        assert g.user.username == "testing"


@pytest.mark.parametrize(
    ("email", "password", "message"),
    (
        ("a@email.com", "test", b"Incorrect email address."),
        ("testing@email.com", "aa", b"Incorrect password."),
    ),
)
def test_login_validate_input(auth, email, password, message, init_db):
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
