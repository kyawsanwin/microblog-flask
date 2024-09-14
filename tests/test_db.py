from microblog import db
from microblog.auth.models import User


def test_db_create(app, init_db):
    user = User(
        username="testing1",
        email="testing1@email.com",
        password="pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f",
    )
    db.session.add(user)
    db.session.commit()

    assert db.session.execute(
        db.select(User).filter_by(username="testing1")
    ).scalar_one()
