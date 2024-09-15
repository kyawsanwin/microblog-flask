from microblog import db
from microblog.blog.models import Blog


def test_blog_index(client, init_db):
    response = client.get("/blog")
    assert response.status_code == 200
    assert b"Blog" in response.data
    assert b"New" in response.data
    assert b"Blog title one" in response.data
    assert b"Blog title two" in response.data


def test_create_page(client, app, auth, init_db):
    response = client.get("/blog/create")
    assert response.status_code == 302
    assert response.headers["Location"] == "/auth/login"


def test_create(client, app, auth, init_db):
    auth.login()
    assert client.get("/blog/create").status_code == 200
    response = client.post(
        "/blog/create",
        data={"title": "Blog title three", "content": "This is blog content."},
    )
    assert response.headers["Location"] == "/blog"

    with app.app_context():
        count = db.session.query(Blog).count()
        assert count == 3
