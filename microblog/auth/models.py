from datetime import datetime, timezone
from typing import List, Optional
from microblog import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    email: Mapped[str] = mapped_column(String(125), unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        default=lambda: datetime.now(timezone.utc)
    )

    todos: Mapped[List["Todo"]] = relationship(  # noqa: F821
        back_populates="user", cascade="all, delete-orphan"
    )

    blogs: Mapped[List["Blog"]] = relationship(back_populates="user")  # noqa: F821

    def __repr__(self) -> str:
        return f"User({self.id}, {self.username}, {self.email})"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
